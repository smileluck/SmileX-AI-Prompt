// md2pdf typst template - 中文文档 PDF 模板
#set page(paper: "a4", margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm))
#set text(font: ("New Computer Modern", "Microsoft YaHei"), size: 11pt, lang: "zh")
#set par(leading: 0.8em, justify: true)
#show heading: set text(font: ("New Computer Modern", "Microsoft YaHei"), weight: "bold")
#show link: set text(fill: blue)

// pandoc 生成内容需要的变量定义
#let horizontalrule = line(length: 100%, stroke: 0.5pt + gray)

$body$
