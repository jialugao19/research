from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from latex2mathml.converter import convert
from markdown_it import MarkdownIt

from .knowledge_sync import KnowledgeSyncError, validate_quant_snapshot, validate_snapshot


@dataclass(frozen=True)
class KnowledgeRelation:
    source: str
    target: str
    type: str
    confidence: float


@dataclass(frozen=True)
class KnowledgeConcept:
    id: str
    name: str
    domain: str
    level: str
    definition: str
    aliases: tuple[str, ...]
    confidence: float
    article_slug: str


@dataclass(frozen=True)
class KnowledgeArticle:
    slug: str
    title: str
    concepts: tuple[str, ...]
    domain: str
    level: str
    content_type: str
    depth_level: str
    keywords: tuple[str, ...]
    review_state: str
    references: tuple[dict[str, str], ...]
    quality: dict[str, float]
    body: str

    @property
    def summary(self) -> str:
        paragraphs = [item.strip() for item in self.body.split("\n\n") if item.strip()]
        for paragraph in paragraphs:
            if not paragraph.startswith(("#", "关键词：", "-", "$$", "```")):
                return re.sub(r"[*`_]", "", paragraph)
        return self.title


@dataclass(frozen=True)
class KnowledgeStage:
    name: str
    topic_ids: tuple[str, ...]
    title: str = ""
    summary: str = ""


@dataclass(frozen=True)
class KnowledgePath:
    id: str
    name: str
    stages: tuple[KnowledgeStage, ...]
    summary: str = ""
    organization: str = ""
    inspiration: str = ""

    @property
    def concept_count(self) -> int:
        return len({topic for stage in self.stages for topic in stage.topic_ids})


@dataclass(frozen=True)
class QuantKnowledgeSection:
    id: str
    sequence: int
    title: str
    directory: str
    chapter_count: int


@dataclass(frozen=True)
class QuantKnowledgeChapter:
    slug: str
    sequence: int
    title: str
    section_id: str
    section_title: str
    source_path: str
    body: str
    part_id: str = ""
    part_title: str = ""

    @property
    def summary(self) -> str:
        paragraphs = [item.strip() for item in self.body.split("\n\n") if item.strip()]
        for paragraph in paragraphs:
            if not paragraph.startswith(("#", "```", "-", "$$")):
                return re.sub(r"[*`_]", "", paragraph)
        return self.title


@dataclass(frozen=True)
class KnowledgeTopic:
    id: str
    title: str
    summary: str
    domain_id: str
    sequence: int

    @property
    def route(self) -> str:
        return f"knowledge/{self.domain_id}/{self.id}/"


@dataclass(frozen=True)
class KnowledgeDomain:
    id: str
    title: str
    summary: str
    sequence: int
    topics: tuple[KnowledgeTopic, ...]

    @property
    def route(self) -> str:
        return f"knowledge/{self.id}/"


@dataclass(frozen=True)
class KnowledgeResearchLink:
    domain_id: str
    topic_id: str
    project: str
    label: str
    summary: str


@dataclass(frozen=True)
class KnowledgeOntology:
    domains: tuple[KnowledgeDomain, ...]
    deepml_domain_map: dict[str, tuple[str, str]]
    quant_section_map: dict[str, tuple[str, str]]
    quant_chapter_rules: tuple[dict[str, Any], ...]
    research_links: tuple[KnowledgeResearchLink, ...]
    domain_by_id: dict[str, KnowledgeDomain] = field(init=False, repr=False)
    topic_by_key: dict[tuple[str, str], KnowledgeTopic] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "domain_by_id", {domain.id: domain for domain in self.domains})
        object.__setattr__(
            self,
            "topic_by_key",
            {(topic.domain_id, topic.id): topic for domain in self.domains for topic in domain.topics},
        )

    def topic(self, domain_id: str, topic_id: str) -> KnowledgeTopic:
        return self.topic_by_key[(domain_id, topic_id)]


@dataclass(frozen=True)
class KnowledgeNode:
    id: str
    slug: str
    title: str
    domain_id: str
    domain_title: str
    topic_id: str
    topic_title: str
    level: str
    content_type: str
    source_id: str
    source_label: str
    summary: str
    body: str
    keywords: tuple[str, ...]
    source_ref: str
    quality: dict[str, float] = field(default_factory=dict)
    aliases: tuple[str, ...] = ()
    concept_ids: tuple[str, ...] = ()
    source_domain: str = ""
    source_part: str = ""

    @property
    def route(self) -> str:
        return f"knowledge/{self.domain_id}/{self.topic_id}/{self.slug}/"


@dataclass(frozen=True)
class KnowledgeCatalog:
    concepts: tuple[KnowledgeConcept, ...]
    articles: tuple[KnowledgeArticle, ...]
    relations: tuple[KnowledgeRelation, ...]
    paths: tuple[KnowledgePath, ...]
    snapshot: dict[str, Any]
    quant_sections: tuple[QuantKnowledgeSection, ...] = ()
    chapters: tuple[QuantKnowledgeChapter, ...] = ()
    quant_snapshot: dict[str, Any] = field(default_factory=dict)
    ontology: KnowledgeOntology | None = None
    nodes: tuple[KnowledgeNode, ...] = ()
    concept_by_id: dict[str, KnowledgeConcept] = field(init=False, repr=False)
    article_by_slug: dict[str, KnowledgeArticle] = field(init=False, repr=False)
    path_by_id: dict[str, KnowledgePath] = field(init=False, repr=False)
    chapter_by_slug: dict[str, QuantKnowledgeChapter] = field(init=False, repr=False)
    node_by_id: dict[str, KnowledgeNode] = field(init=False, repr=False)
    node_by_slug: dict[str, KnowledgeNode] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "concept_by_id", {item.id: item for item in self.concepts})
        object.__setattr__(self, "article_by_slug", {item.slug: item for item in self.articles})
        object.__setattr__(self, "path_by_id", {item.id: item for item in self.paths})
        object.__setattr__(self, "chapter_by_slug", {item.slug: item for item in self.chapters})
        object.__setattr__(self, "node_by_id", {item.id: item for item in self.nodes})
        object.__setattr__(self, "node_by_slug", {item.slug: item for item in self.nodes})

    @property
    def counts(self) -> dict[str, int]:
        return {
            "concepts": len(self.concepts),
            "articles": len(self.articles),
            "relations": len(self.relations),
            "paths": len(self.paths),
        }

    @property
    def aggregate_counts(self) -> dict[str, int]:
        return {
            "sources": 2 if self.chapters else 1,
            "concepts": len(self.concepts),
            "deepml_articles": len(self.articles),
            "quant_chapters": len(self.chapters),
            "nodes": len(self.nodes),
            "relations": len(self.relations),
            "paths": len(self.paths),
        }

    @property
    def domains(self) -> tuple[tuple[str, int], ...]:
        counts: dict[str, int] = {}
        for concept in self.concepts:
            counts[concept.domain] = counts.get(concept.domain, 0) + 1
        return tuple(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

    @property
    def ontology_domains(self) -> tuple[KnowledgeDomain, ...]:
        return self.ontology.domains if self.ontology is not None else ()

    def nodes_for_domain(self, domain_id: str) -> tuple[KnowledgeNode, ...]:
        return tuple(node for node in self.nodes if node.domain_id == domain_id)

    def nodes_for_topic(self, domain_id: str, topic_id: str) -> tuple[KnowledgeNode, ...]:
        return tuple(node for node in self.nodes if node.domain_id == domain_id and node.topic_id == topic_id)

    def research_links_for(self, domain_id: str, topic_id: str | None = None) -> tuple[KnowledgeResearchLink, ...]:
        if self.ontology is None:
            return ()
        return tuple(
            link
            for link in self.ontology.research_links
            if link.domain_id == domain_id and (topic_id is None or link.topic_id == topic_id)
        )

    def prerequisite_nodes_for(self, node_id: str) -> tuple[KnowledgeNode, ...]:
        ids = [item.source for item in self.relations if item.type == "prerequisite_of" and item.target == node_id]
        return self._nodes(ids)

    def next_nodes_for(self, node_id: str) -> tuple[KnowledgeNode, ...]:
        ids = [item.target for item in self.relations if item.type == "prerequisite_of" and item.source == node_id]
        return self._nodes(ids)

    def related_nodes_for(self, node_id: str) -> tuple[KnowledgeNode, ...]:
        ids: list[str] = []
        for relation in self.relations:
            if relation.type not in {"related", "part_of", "used_with", "contrasts_with"}:
                continue
            if relation.source == node_id:
                ids.append(relation.target)
            elif relation.target == node_id:
                ids.append(relation.source)
        return self._nodes(ids)

    def prerequisites_for(self, concept_id: str) -> tuple[KnowledgeConcept, ...]:
        ids = [item.source for item in self.relations if item.type == "prerequisite_of" and item.target == concept_id]
        return self._concepts(ids)

    def next_concepts_for(self, concept_id: str) -> tuple[KnowledgeConcept, ...]:
        ids = [item.target for item in self.relations if item.type == "prerequisite_of" and item.source == concept_id]
        return self._concepts(ids)

    def related_for(self, concept_id: str) -> tuple[KnowledgeConcept, ...]:
        ids: list[str] = []
        for relation in self.relations:
            if relation.type not in {"related", "part_of", "used_with", "contrasts_with"}:
                continue
            if relation.source == concept_id:
                ids.append(relation.target)
            elif relation.target == concept_id:
                ids.append(relation.source)
        return self._concepts(ids)

    def _concepts(self, ids: list[str]) -> tuple[KnowledgeConcept, ...]:
        seen: set[str] = set()
        values: list[KnowledgeConcept] = []
        for concept_id in ids:
            if concept_id in seen or concept_id not in self.concept_by_id:
                continue
            seen.add(concept_id)
            values.append(self.concept_by_id[concept_id])
        return tuple(values)

    def _nodes(self, ids: list[str]) -> tuple[KnowledgeNode, ...]:
        seen: set[str] = set()
        values: list[KnowledgeNode] = []
        for node_id in ids:
            if node_id in seen or node_id not in self.node_by_id:
                continue
            seen.add(node_id)
            values.append(self.node_by_id[node_id])
        return tuple(values)


@dataclass(frozen=True)
class RenderedKnowledgeArticle:
    html: str
    toc: tuple[dict[str, str], ...]


def load_knowledge(
    snapshot_root: Path,
    quant_snapshot_root: Path | None = None,
    ontology_path: Path | None = None,
) -> KnowledgeCatalog:
    snapshot = validate_snapshot(snapshot_root)
    if ontology_path is None:
        raise KnowledgeSyncError("knowledge ontology path is required")
    ontology = _load_ontology(ontology_path)
    concepts_payload = _load_yaml(snapshot_root / "graph" / "concepts.yaml")
    units_payload = _load_yaml(snapshot_root / "graph" / "learning_units.yaml")
    article_by_concept = {
        str(item["concept_id"]): Path(str(item["article"])).stem
        for item in units_payload.get("learning_units", [])
        if isinstance(item, dict) and item.get("article")
    }
    concepts = tuple(
        KnowledgeConcept(
            id=str(item["id"]),
            name=str(item["name"]),
            domain=str(item["domain"]),
            level=str(item["level"]),
            definition=str(item["definition"]),
            aliases=tuple(str(value) for value in item.get("aliases", [])),
            confidence=float(item["confidence"]),
            article_slug=article_by_concept[str(item["id"])],
        )
        for item in concepts_payload.get("concepts", [])
    )
    quality_by_slug = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))["score"]
        for path in (snapshot_root / "quality").glob("*.json")
        if path.name != "discovery_snapshot.json"
    }
    articles: list[KnowledgeArticle] = []
    for path in sorted((snapshot_root / "articles").glob("*.md")):
        metadata, body = _parse_front_matter(path)
        references = metadata.get("references", [])
        review = metadata.get("review", {})
        articles.append(
            KnowledgeArticle(
                slug=str(metadata["slug"]),
                title=str(metadata["title"]),
                concepts=tuple(str(value) for value in metadata.get("concepts", [])),
                domain=str(metadata["domain"]),
                level=str(metadata["level"]),
                content_type=str(metadata["content_type"]),
                depth_level=str(metadata["depth_level"]),
                keywords=tuple(str(value) for value in metadata.get("keywords", [])),
                review_state=str(review.get("state", "")),
                references=tuple(
                    {"title": str(item["title"]), "url": str(item["url"]), "type": str(item["type"])}
                    for item in references
                    if isinstance(item, dict)
                ),
                quality={str(key): float(value) for key, value in quality_by_slug[path.stem].items()},
                body=body,
            )
        )
    relations = tuple(
        KnowledgeRelation(
            source=str(item["source"]),
            target=str(item["target"]),
            type=str(item["type"]),
            confidence=float(item["confidence"]),
        )
        for item in _load_jsonl(snapshot_root / "graph" / "relations.jsonl")
    )
    paths: list[KnowledgePath] = []
    for path in sorted((snapshot_root / "paths").glob("*.yaml")):
        payload = _load_yaml(path)
        stages = tuple(
            KnowledgeStage(
                name=str(stage.get("name", "Stage")),
                topic_ids=tuple(str(value) for value in stage.get("topics", [])),
                title=str(stage.get("title", stage.get("name", "Stage"))),
                summary=str(stage.get("summary", "")),
            )
            for stage in payload.get("stages", [])
            if isinstance(stage, dict)
        )
        path_meta = payload.get("path", {})
        paths.append(
            KnowledgePath(
                id=path.stem,
                name=str(path_meta.get("name", path.stem)),
                stages=stages,
                summary=str(path_meta.get("summary", "")),
                organization=str(path_meta.get("organization", "")),
                inspiration=str(path_meta.get("inspiration", "")),
            )
        )
    quant_sections: tuple[QuantKnowledgeSection, ...] = ()
    chapters: tuple[QuantKnowledgeChapter, ...] = ()
    quant_snapshot: dict[str, Any] = {}
    if quant_snapshot_root is not None:
        quant_snapshot = validate_quant_snapshot(quant_snapshot_root)
        quant_sections, chapters = _load_quant_knowledge(quant_snapshot_root, quant_snapshot)
    nodes = _build_nodes(
        ontology=ontology,
        concepts=concepts,
        articles=tuple(articles),
        chapters=chapters,
    )
    knowledge = KnowledgeCatalog(
        concepts=concepts,
        articles=tuple(articles),
        relations=relations,
        paths=tuple(paths),
        snapshot=snapshot,
        quant_sections=quant_sections,
        chapters=chapters,
        quant_snapshot=quant_snapshot,
        ontology=ontology,
        nodes=nodes,
    )
    _validate_knowledge(knowledge)
    return knowledge


def render_knowledge_markdown(article: KnowledgeArticle) -> RenderedKnowledgeArticle:
    return _render_markdown_document(article.title, article.body, f"article {article.slug}")


def render_quant_chapter_markdown(chapter: QuantKnowledgeChapter) -> RenderedKnowledgeArticle:
    return _render_markdown_document(chapter.title, chapter.body, f"chapter {chapter.slug}")


def render_knowledge_node_markdown(node: KnowledgeNode) -> RenderedKnowledgeArticle:
    return _render_markdown_document(node.title, node.body, f"node {node.id}")


def _render_markdown_document(title: str, body: str, context: str) -> RenderedKnowledgeArticle:
    math_blocks: list[str] = []

    def replace_math(match: re.Match[str]) -> str:
        expression = match.group(1).strip()
        token = f"DEEPMATHBLOCK{len(math_blocks):04d}"
        try:
            math_blocks.append(convert(expression))
        except Exception as exc:
            raise KnowledgeSyncError(f"{context} contains invalid display math") from exc
        return f"\n\n{token}\n\n"

    source = re.sub(r"^#\s+.+?\n+", "", body, count=1)
    markdown = re.sub(r"\$\$\s*(.*?)\s*\$\$", replace_math, source, flags=re.DOTALL)
    markdown = re.sub(r"(?<![\[(])(https?://[^\s。]+)", r"[\1](\1)", markdown)
    heading_titles = re.findall(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    toc = tuple({"id": f"chapter-{index:02d}", "title": title} for index, title in enumerate(heading_titles, 1))
    renderer = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": False})
    rendered = renderer.render(markdown)
    for item in toc:
        rendered = rendered.replace("<h2>", f'<h2 id="{item["id"]}">', 1)
    for index, mathml in enumerate(math_blocks):
        token = f"DEEPMATHBLOCK{index:04d}"
        rendered = rendered.replace(f"<p>{token}</p>", f'<div class="math-block" role="math">{mathml}</div>')
    return RenderedKnowledgeArticle(html=rendered, toc=toc)


def _load_ontology(path: Path) -> KnowledgeOntology:
    payload = _load_yaml(path)
    if payload.get("schema_version") != 1:
        raise KnowledgeSyncError("knowledge ontology has unsupported schema_version")
    domains_payload = payload.get("domains", [])
    if not isinstance(domains_payload, list) or not domains_payload:
        raise KnowledgeSyncError("knowledge ontology must define domains")
    domains: list[KnowledgeDomain] = []
    for domain_index, domain_payload in enumerate(domains_payload, 1):
        if not isinstance(domain_payload, dict):
            raise KnowledgeSyncError("knowledge ontology domains must be mappings")
        topics_payload = domain_payload.get("topics", [])
        if not isinstance(topics_payload, list) or not topics_payload:
            raise KnowledgeSyncError(f"knowledge domain {domain_payload.get('id')} must define topics")
        domain_id = str(domain_payload["id"])
        topics = tuple(
            KnowledgeTopic(
                id=str(topic_payload["id"]),
                title=str(topic_payload["title"]),
                summary=str(topic_payload["summary"]),
                domain_id=domain_id,
                sequence=topic_index,
            )
            for topic_index, topic_payload in enumerate(topics_payload, 1)
            if isinstance(topic_payload, dict)
        )
        domains.append(
            KnowledgeDomain(
                id=domain_id,
                title=str(domain_payload["title"]),
                summary=str(domain_payload["summary"]),
                sequence=domain_index,
                topics=topics,
            )
        )
    ontology = KnowledgeOntology(
        domains=tuple(domains),
        deepml_domain_map=_load_topic_map(payload.get("deepml_domain_map", {}), "deepml_domain_map"),
        quant_section_map=_load_topic_map(payload.get("quant_section_map", {}), "quant_section_map"),
        quant_chapter_rules=_load_chapter_rules(payload.get("quant_chapter_rules", [])),
        research_links=_load_research_links(payload.get("research_links", [])),
    )
    _validate_ontology(ontology)
    return ontology


def _build_nodes(
    ontology: KnowledgeOntology,
    concepts: tuple[KnowledgeConcept, ...],
    articles: tuple[KnowledgeArticle, ...],
    chapters: tuple[QuantKnowledgeChapter, ...],
) -> tuple[KnowledgeNode, ...]:
    article_by_slug = {article.slug: article for article in articles}
    nodes: list[KnowledgeNode] = []
    for concept in concepts:
        article = article_by_slug[concept.article_slug]
        domain_id, topic_id = _ontology_mapping_for_deepml(ontology, concept.domain)
        topic = ontology.topic(domain_id, topic_id)
        domain = ontology.domain_by_id[domain_id]
        nodes.append(
            KnowledgeNode(
                id=concept.id,
                slug=concept.id,
                title=concept.name,
                domain_id=domain.id,
                domain_title=domain.title,
                topic_id=topic.id,
                topic_title=topic.title,
                level=concept.level,
                content_type="Concept",
                source_id="deep-ml",
                source_label="DeepML",
                summary=concept.definition,
                body=article.body,
                keywords=tuple(dict.fromkeys((*concept.aliases, *article.keywords))),
                source_ref=f"articles/{article.slug}.md",
                quality=article.quality,
                aliases=concept.aliases,
                concept_ids=(concept.id,),
                source_domain=concept.domain,
            )
        )
    for chapter in chapters:
        domain_id, topic_id = _ontology_mapping_for_chapter(ontology, chapter)
        topic = ontology.topic(domain_id, topic_id)
        domain = ontology.domain_by_id[domain_id]
        nodes.append(
            KnowledgeNode(
                id=chapter.slug,
                slug=chapter.slug,
                title=chapter.title,
                domain_id=domain.id,
                domain_title=domain.title,
                topic_id=topic.id,
                topic_title=topic.title,
                level=_chapter_level(chapter),
                content_type="Chapter",
                source_id="quant-knowledge",
                source_label="Quant Knowledge",
                summary=chapter.summary,
                body=chapter.body,
                keywords=tuple(
                    value for value in (chapter.section_title, chapter.part_title, chapter.source_path) if value
                ),
                source_ref=chapter.source_path,
                source_domain=chapter.section_id,
                source_part=chapter.part_title,
            )
        )
    return tuple(sorted(nodes, key=lambda node: (node.domain_id, node.topic_id, node.title.lower(), node.id)))


def knowledge_payload(knowledge: KnowledgeCatalog, base_url: str) -> dict[str, Any]:
    if knowledge.ontology is None:
        raise KnowledgeSyncError("knowledge payload requires ontology")
    return {
        "schema_version": 3,
        "counts": knowledge.aggregate_counts,
        "source_hashes": knowledge.snapshot["source_hashes"],
        "sources": [
            {
                "id": "deep-ml",
                "name": "DeepML",
                "type": "concept_graph",
                "counts": knowledge.counts,
            },
            {
                "id": "quant-knowledge",
                "name": "Quant Knowledge",
                "type": "chapter_booklet",
                "counts": {
                    "sections": len(knowledge.quant_sections),
                    "chapters": len(knowledge.chapters),
                },
            },
        ],
        "domains": [
            {
                "id": domain.id,
                "title": domain.title,
                "summary": domain.summary,
                "url": f"{base_url}{domain.route}",
                "topic_count": len(domain.topics),
                "node_count": len(knowledge.nodes_for_domain(domain.id)),
            }
            for domain in knowledge.ontology.domains
        ],
        "topics": [
            {
                "id": topic.id,
                "title": topic.title,
                "summary": topic.summary,
                "domain": topic.domain_id,
                "url": f"{base_url}{topic.route}",
                "node_count": len(knowledge.nodes_for_topic(topic.domain_id, topic.id)),
            }
            for domain in knowledge.ontology.domains
            for topic in domain.topics
        ],
        "nodes": [
            {
                "id": node.id,
                "slug": node.slug,
                "title": node.title,
                "domain": node.domain_id,
                "topic": node.topic_id,
                "level": node.level,
                "content_type": node.content_type,
                "source": node.source_id,
                "source_ref": node.source_ref,
                "source_part": node.source_part,
                "url": f"{base_url}{node.route}",
            }
            for node in knowledge.nodes
        ],
        "relations": [
            {
                "source": item.source,
                "target": item.target,
                "type": item.type,
                "confidence": item.confidence,
            }
            for item in knowledge.relations
            if item.source in knowledge.node_by_id and item.target in knowledge.node_by_id
        ],
        "research_links": [
            {
                "domain": link.domain_id,
                "topic": link.topic_id,
                "project": link.project,
                "label": link.label,
                "summary": link.summary,
                "url": f"{base_url}projects/{link.project}/",
            }
            for link in knowledge.ontology.research_links
        ],
    }


def _load_topic_map(value: Any, context: str) -> dict[str, tuple[str, str]]:
    if not isinstance(value, dict):
        raise KnowledgeSyncError(f"{context} must be a mapping")
    mapping: dict[str, tuple[str, str]] = {}
    for key, raw_target in value.items():
        if not isinstance(raw_target, list) or len(raw_target) != 2:
            raise KnowledgeSyncError(f"{context}.{key} must be [domain, topic]")
        mapping[str(key)] = (str(raw_target[0]), str(raw_target[1]))
    return mapping


def _load_chapter_rules(value: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, list):
        raise KnowledgeSyncError("quant_chapter_rules must be a list")
    rules: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise KnowledgeSyncError(f"quant_chapter_rules[{index}] must be a mapping")
        rules.append(
            {
                "prefixes": tuple(str(prefix) for prefix in item.get("prefixes", [])),
                "slugs": tuple(str(slug) for slug in item.get("slugs", [])),
                "domain": str(item["domain"]),
                "topic": str(item["topic"]),
            }
        )
    return tuple(rules)


def _load_research_links(value: Any) -> tuple[KnowledgeResearchLink, ...]:
    if not isinstance(value, list):
        raise KnowledgeSyncError("research_links must be a list")
    links: list[KnowledgeResearchLink] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise KnowledgeSyncError(f"research_links[{index}] must be a mapping")
        links.append(
            KnowledgeResearchLink(
                domain_id=str(item["domain"]),
                topic_id=str(item["topic"]),
                project=str(item["project"]),
                label=str(item["label"]),
                summary=str(item["summary"]),
            )
        )
    return tuple(links)


def _validate_ontology(ontology: KnowledgeOntology) -> None:
    for context, mappings in (
        ("deepml_domain_map", ontology.deepml_domain_map),
        ("quant_section_map", ontology.quant_section_map),
    ):
        for key, mapping in mappings.items():
            if mapping not in ontology.topic_by_key:
                raise KnowledgeSyncError(f"{context}.{key} references unknown topic {mapping}")
    for index, rule in enumerate(ontology.quant_chapter_rules):
        mapping = (str(rule["domain"]), str(rule["topic"]))
        if mapping not in ontology.topic_by_key:
            raise KnowledgeSyncError(f"quant_chapter_rules[{index}] references unknown topic {mapping}")
    for link in ontology.research_links:
        if (link.domain_id, link.topic_id) not in ontology.topic_by_key:
            raise KnowledgeSyncError(f"research link {link.label} references unknown topic")


def _ontology_mapping_for_deepml(ontology: KnowledgeOntology, source_domain: str) -> tuple[str, str]:
    if source_domain not in ontology.deepml_domain_map:
        raise KnowledgeSyncError(f"DeepML domain {source_domain} is missing from ontology")
    return ontology.deepml_domain_map[source_domain]


def _ontology_mapping_for_chapter(
    ontology: KnowledgeOntology,
    chapter: QuantKnowledgeChapter,
) -> tuple[str, str]:
    for rule in ontology.quant_chapter_rules:
        if chapter.slug in rule["slugs"]:
            return str(rule["domain"]), str(rule["topic"])
    best_match: tuple[int, tuple[str, str]] | None = None
    for rule in ontology.quant_chapter_rules:
        for prefix in rule["prefixes"]:
            if chapter.slug.startswith(prefix) and (best_match is None or len(prefix) > best_match[0]):
                best_match = (len(prefix), (str(rule["domain"]), str(rule["topic"])))
    if best_match is not None:
        return best_match[1]
    if chapter.section_id not in ontology.quant_section_map:
        raise KnowledgeSyncError(f"Quant section {chapter.section_id} is missing from ontology")
    return ontology.quant_section_map[chapter.section_id]


def _chapter_level(chapter: QuantKnowledgeChapter) -> str:
    if chapter.section_id in {"01-python", "08-computer-science"}:
        return "engineering"
    if chapter.section_id in {"02-probability-timeseries", "04-brain-teaser-green-book"}:
        return "foundation"
    if chapter.section_id == "07-market-microstructure":
        return "applied"
    return "practice"


def _validate_knowledge(knowledge: KnowledgeCatalog) -> None:
    if knowledge.ontology is None:
        raise KnowledgeSyncError("knowledge ontology is required")
    counts = knowledge.snapshot.get("counts", {})
    if knowledge.counts != {key: counts.get(key) for key in ("concepts", "articles", "relations", "paths")}:
        raise KnowledgeSyncError("knowledge snapshot counts do not match loaded records")
    concept_ids = set(knowledge.concept_by_id)
    article_slugs = set(knowledge.article_by_slug)
    for concept in knowledge.concepts:
        if concept.article_slug not in article_slugs:
            raise KnowledgeSyncError(f"concept {concept.id} references missing article {concept.article_slug}")
    for article in knowledge.articles:
        if article.review_state not in {"automated_editorial", "approved"}:
            raise KnowledgeSyncError(f"article {article.slug} is not publishable")
        unknown = set(article.concepts) - concept_ids
        if unknown:
            raise KnowledgeSyncError(f"article {article.slug} references unknown concepts {sorted(unknown)[:3]}")
    for relation in knowledge.relations:
        if relation.source not in concept_ids or relation.target not in concept_ids:
            raise KnowledgeSyncError(f"relation references unknown concept: {relation}")
    for path in knowledge.paths:
        unknown = {topic for stage in path.stages for topic in stage.topic_ids} - concept_ids
        if unknown:
            raise KnowledgeSyncError(f"path {path.id} references unknown concepts {sorted(unknown)[:3]}")
    source_domains = {concept.domain for concept in knowledge.concepts}
    missing_domains = source_domains - set(knowledge.ontology.deepml_domain_map)
    if missing_domains:
        raise KnowledgeSyncError("DeepML domains missing from ontology: " + ", ".join(sorted(missing_domains)[:5]))
    if knowledge.quant_snapshot:
        quant_counts = knowledge.quant_snapshot.get("counts", {})
        if len(knowledge.quant_sections) != quant_counts.get("sections"):
            raise KnowledgeSyncError("quant knowledge section count does not match snapshot")
        if len(knowledge.chapters) != quant_counts.get("chapters"):
            raise KnowledgeSyncError("quant knowledge chapter count does not match snapshot")
        section_ids = {section.id for section in knowledge.quant_sections}
        if len(knowledge.chapter_by_slug) != len(knowledge.chapters):
            raise KnowledgeSyncError("quant knowledge chapter slugs must be unique")
        for chapter in knowledge.chapters:
            if chapter.section_id not in section_ids:
                raise KnowledgeSyncError(f"chapter {chapter.slug} references unknown section {chapter.section_id}")
            if not chapter.body.startswith("# "):
                raise KnowledgeSyncError(f"chapter {chapter.slug} is missing its H1 title")
            if "\n## " not in chapter.body:
                raise KnowledgeSyncError(f"chapter {chapter.slug} is missing H2 sections")
        source_sections = {chapter.section_id for chapter in knowledge.chapters}
        missing_sections = source_sections - set(knowledge.ontology.quant_section_map)
        if missing_sections:
            raise KnowledgeSyncError("Quant sections missing from ontology: " + ", ".join(sorted(missing_sections)[:5]))
    if len(knowledge.node_by_id) != len(knowledge.nodes):
        raise KnowledgeSyncError("knowledge node ids must be unique")
    if len(knowledge.node_by_slug) != len(knowledge.nodes):
        raise KnowledgeSyncError("knowledge node slugs must be unique")
    routes = [node.route for node in knowledge.nodes]
    if len(routes) != len(set(routes)):
        raise KnowledgeSyncError("knowledge node routes must be unique")
    topic_keys = set(knowledge.ontology.topic_by_key)
    for node in knowledge.nodes:
        if (node.domain_id, node.topic_id) not in topic_keys:
            raise KnowledgeSyncError(f"node {node.id} references unknown ontology topic")


def _load_quant_knowledge(
    snapshot_root: Path,
    snapshot: dict[str, Any],
) -> tuple[tuple[QuantKnowledgeSection, ...], tuple[QuantKnowledgeChapter, ...]]:
    sections_payload = snapshot.get("sections", [])
    if not isinstance(sections_payload, list):
        raise KnowledgeSyncError("quant knowledge sections must be a list")
    sections = tuple(
        QuantKnowledgeSection(
            id=str(item["id"]),
            sequence=int(item["sequence"]),
            title=str(item["title"]),
            directory=str(item["directory"]),
            chapter_count=int(item["chapter_count"]),
        )
        for item in sections_payload
        if isinstance(item, dict)
    )
    chapters_payload = snapshot.get("chapters", [])
    if not isinstance(chapters_payload, list):
        raise KnowledgeSyncError("quant knowledge chapters must be a list")
    chapters: list[QuantKnowledgeChapter] = []
    for item in chapters_payload:
        if not isinstance(item, dict):
            continue
        source_path = str(item["source_path"])
        body_path = snapshot_root / source_path
        if not body_path.is_file():
            raise KnowledgeSyncError(f"quant knowledge chapter file is missing: {source_path}")
        chapters.append(
            QuantKnowledgeChapter(
                slug=str(item["slug"]),
                sequence=int(item["sequence"]),
                title=str(item["title"]),
                section_id=str(item["section_id"]),
                section_title=str(item["section_title"]),
                source_path=source_path,
                body=body_path.read_text(encoding="utf-8").strip(),
                part_id=str(item.get("part_id", "")),
                part_title=str(item.get("part_title", "")),
            )
        )
    return sections, tuple(sorted(chapters, key=lambda item: item.sequence))


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise KnowledgeSyncError(f"{path} must contain a YAML mapping")
    return value


def _load_jsonl(path: Path) -> tuple[dict[str, Any], ...]:
    return tuple(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _parse_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise KnowledgeSyncError(f"{path} is missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise KnowledgeSyncError(f"{path} has unterminated front matter")
    metadata = yaml.safe_load(text[4:end])
    if not isinstance(metadata, dict):
        raise KnowledgeSyncError(f"{path} front matter must be a mapping")
    return metadata, text[end + 5 :].strip()
