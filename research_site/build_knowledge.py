from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment
from markupsafe import Markup

from research_site.build_output import write_text
from research_site.catalog import Catalog, CatalogError
from research_site.knowledge import KnowledgeCatalog, render_knowledge_node_markdown


def _related_concept_rows(
    knowledge: KnowledgeCatalog,
    node_id: str,
    source_groups: tuple[tuple[str, ...], ...],
) -> tuple[tuple[dict[str, str], ...], ...]:
    groups = source_groups
    if not groups:
        groups = tuple(
            tuple(item.title for item in items)
            for items in (
                knowledge.prerequisite_nodes_for(node_id),
                knowledge.related_nodes_for(node_id),
                knowledge.next_nodes_for(node_id),
            )
            if items
        )
    rows: list[tuple[dict[str, str], ...]] = []
    for group in groups[:3]:
        cards: list[dict[str, str]] = []
        for title in group:
            target = knowledge.node_for_title(title)
            if target is not None and target.id == node_id:
                continue
            cards.append({"title": title, "route": target.route if target is not None else ""})
        if cards:
            rows.append(tuple(cards))
    return tuple(rows)


def render_knowledge_pages(
    catalog: Catalog,
    environment: Environment,
    output_root: Path,
    base_url: str,
    common: dict[str, Any],
) -> KnowledgeCatalog:
    if catalog.knowledge is None:
        raise CatalogError("catalog is missing the knowledge graph snapshot")
    knowledge = catalog.knowledge
    knowledge_home = environment.get_template("knowledge.html").render(
        **common,
        active_project=None,
        active_report=None,
        active_domain=None,
        active_topic=None,
        active_subtopic=None,
        nav_section="knowledge",
    )
    write_text(output_root / "knowledge" / "index.html", knowledge_home)
    domain_template = environment.get_template("knowledge_domain.html")
    topic_template = environment.get_template("knowledge_topic.html")
    node_template = environment.get_template("knowledge_node.html")
    for domain in knowledge.ontology_domains:
        write_text(
            output_root / domain.route / "index.html",
            domain_template.render(
                **common,
                active_project=None,
                active_report=None,
                active_domain=domain.id,
                active_topic=None,
                active_subtopic=None,
                nav_section="knowledge",
                domain=domain,
                nodes=knowledge.nodes_for_domain(domain.id),
                research_links=knowledge.research_links_for(domain.id),
            ),
        )
        for topic in domain.topics:
            learning_path = (
                knowledge.path_by_id.get("deep-learning-engineer")
                if domain.id == "machine-intelligence" and topic.id == "deep-learning"
                else None
            )
            deep_learning_chapters = (
                tuple(
                    chapter
                    for chapter in knowledge.chapters
                    if chapter.section_id == "06-deep-learning" and chapter.part_title
                )
                if learning_path is not None
                else ()
            )
            chapter_parts = tuple(
                sorted(
                    {
                        chapter.part_title: sum(
                            1 for item in deep_learning_chapters if item.part_title == chapter.part_title
                        )
                        for chapter in deep_learning_chapters
                    }.items()
                )
            )
            write_text(
                output_root / topic.route / "index.html",
                topic_template.render(
                    **common,
                    active_project=None,
                    active_report=None,
                    active_domain=domain.id,
                    active_topic=topic.id,
                    active_subtopic=None,
                    nav_section="knowledge",
                    domain=domain,
                    topic=topic,
                    nodes=knowledge.nodes_for_topic(domain.id, topic.id),
                    learning_path=learning_path,
                    chapter_parts=chapter_parts,
                    research_links=knowledge.research_links_for(domain.id, topic.id),
                ),
            )
    for node in knowledge.nodes:
        rendered = render_knowledge_node_markdown(node)
        write_text(
            output_root / node.route / "index.html",
            node_template.render(
                **common,
                active_project=None,
                active_report=None,
                active_domain=node.domain_id,
                active_topic=node.topic_id,
                active_subtopic=node.subtopic_id or None,
                nav_section="knowledge",
                node=node,
                next_page=knowledge.next_page_for(node.id),
                related_rows=_related_concept_rows(knowledge, node.id, rendered.related_groups),
                research_links=knowledge.research_links_for(node.domain_id, node.topic_id),
                body_html=Markup(rendered.html),
                toc=rendered.toc,
            ),
        )
    return knowledge
