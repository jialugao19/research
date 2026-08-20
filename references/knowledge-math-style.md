# Knowledge math style

Knowledge formulas use LaTeX display blocks and must pass
`python3 scripts/audit_knowledge_math.py`. The formula should state the actual
mathematical definition or update rule, not English pseudocode placed between
math delimiters.

## Notation rules

- Use `\Pr`, `\mathbb{E}`, `\operatorname{Var}`, and `\operatorname{Cov}` for
  probability operators.
- Use `\operatorname{arg\,min}` and `\operatorname{arg\,max}` with an explicit
  optimization variable and feasible set when one is required.
- Use `\lVert x\rVert` for norms, `\mid` for conditioning, `\Vert` for
  divergence arguments, and `\ldots` or `\cdots` for ellipses.
- Put descriptive labels and multi-letter subscripts in `\mathrm{}` or
  `\text{}`. Put named functions in `\operatorname{}`.
- State summation or integration limits, parameter constraints, and domains
  whenever omitting them would make the definition ambiguous.
- Distinguish population quantities from estimators with notation such as
  `\mu` versus `\bar x`, `\sigma^2` versus `s^2`, and `\theta` versus
  `\hat\theta`.

## Authoritative references

- NIST/SEMATECH, *e-Handbook of Statistical Methods*:
  https://www.itl.nist.gov/div898/handbook/
- Stanford CS229, *Machine Learning Notes*:
  https://cs229.stanford.edu/main_notes.pdf
- MIT OpenCourseWare 18.06, *Linear Algebra*:
  https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/
- MIT OpenCourseWare 18.S096, *Matrix Calculus for Machine Learning and
  Beyond*: https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/
- Boyd and Vandenberghe, *Convex Optimization*:
  https://web.stanford.edu/~boyd/cvxbook/
- Zhang et al., *Dive into Deep Learning*: https://d2l.ai/
- Sutton and Barto, *Reinforcement Learning: An Introduction*:
  http://incompleteideas.net/book/the-book-2nd.html
- PyTorch reference documentation: https://docs.pytorch.org/docs/stable/
- Hugging Face Transformers documentation:
  https://huggingface.co/docs/transformers/
