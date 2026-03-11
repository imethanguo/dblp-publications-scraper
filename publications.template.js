module.exports = [
    {
        title: "Title of your paper",
        date: "date of publication, e.g., 2021-12-31 or 2021, following ECMA date string format: https://262.ecma-international.org/11.0/#sec-date-time-string-format",
        authors: [
            "First Author", "Second Author"
        ],
        venue: "Full name of the conference or journal name",
        venueShort: "abbreviation of conference or journal, e.g., ESEC/FSE",
        tags: [],
        awards: [],
        abstract: `
            (optional) abstract of your paper (support multiline)
        `,
        arxivUrl: "(optional) the arxiv version of your paper",
        paperUrl: "(optional) author version of your paper. You can put the pdf file in assets folder and refer to it here with {ASSETS}/your-paper.pdf",
        bibtex: ` (optional)
            @article{paper
                ......
            }
        `
    }
]