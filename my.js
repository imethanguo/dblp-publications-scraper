module.exports = [
    {
        "title": "CodeCleaner: Mitigating Data Contamination for LLM Benchmarking.",
        "date": "2025-06-20",
        "authors": [
            "Jialun Cao",
            "Songqiang Chen",
            "Wuqi Zhang",
            "Hau Ching Lo",
            "Yeting Li",
            "Shing-Chi Cheung"
        ],
        "venue": "the 16th International Conference on Internetware",
        "venueShort": "",
        "abstract": "Data contamination presents a critical barrier preventing widespread industrial adoption of advanced software engineering techniques that leverage large language models (LLMs). This phenomenon occurs when evaluation data inadvertently overlaps with the public code repositories used to train LLMs, severely undermining the credibility of performance evaluations. Code refactoring, which comprises code restructuring and variable renaming, has emerged as a promising measure to mitigate data contamination. However, the lack of automated code refactoring tools and scientifically validated refactoring techniques has hampered widespread industrial implementation. To bridge the gap, this paper presents the first systematic study to examine the efficacy of code refactoring operators at multiple scales (method-level, class-level, and cross-class level) and in different programming languages. We develop CodeCleaner, including 11 operators for Python in multiple scales and 4 for Java. We elaborate on the rationale for why these operators could work to resolve data contamination and use both data-wise (e.g., N-gram matching overlap ratio) and model-wise metrics (e.g., perplexity) to quantify the efficacy after operators are applied. A drop of 75% overlap ratio is found when applying all operators in CodeCleaner, demonstrating their effectiveness in addressing data contamination. Besides, we migrate four operators to Java, showing their generalizability to another language. We also observed an average of 19% decrease in LLMs’ performance after applying our operators. We make CodeCleaner online available at https://github.com/ArabelaTso/CodeCleaner-v1 to facilitate further studies on mitigating LLM data contamination.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1145/3755881.3755901",
        "bibtex": "@inproceedings{DBLP:conf/internetware/CaoCZLLC25,\n  author       = {Jialun Cao and\n                  Songqiang Chen and\n                  Wuqi Zhang and\n                  Hau Ching Lo and\n                  Yeting Li and\n                  Shing{-}Chi Cheung},\n  editor       = {Hong Mei and\n                  Jian Lv and\n                  Zhi Jin and\n                  Xuandong Li and\n                  Thomas Zimmermann and\n                  Ge Li and\n                  Lei Bu and\n                  Xin Xia},\n  title        = {CodeCleaner: Mitigating Data Contamination for {LLM} Benchmarking},\n  booktitle    = {Proceedings of the 16th International Conference on Internetware,\n                  Internetware 2025, Trondheim, Norway, June 20-22, 2025},\n  pages        = {71--83},\n  publisher    = {{ACM}},\n  year         = {2025},\n  url          = {https://doi.org/10.1145/3755881.3755901},\n  doi          = {10.1145/3755881.3755901},\n  timestamp    = {Thu, 05 Mar 2026 17:17:59 +0100},\n  biburl       = {https://dblp.org/rec/conf/internetware/CaoCZLLC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "LspFuzz: Hunting Bugs in Language Servers.",
        "date": "2025-11-16",
        "authors": [
            "Hengcheng Zhu",
            "Songqiang Chen",
            "Valerio Terragni",
            "Lili Wei",
            "Yepang Liu",
            "Jiarong Wu",
            "Shing-Chi Cheung"
        ],
        "venue": "40th IEEE/ACM International Conference on Automated Software Engineering",
        "venueShort": "ASE",
        "abstract": "The Language Server Protocol (LSP) has revolutionized the integration of code intelligence in modern software development. There are approximately 300 LSP server implementations for various languages and 50 editors offering LSP integration. However, the reliability of LSP servers is a growing concern, as crashes can disable all code intelligence features and significantly impact productivity, while vulnerabilities can put developers at risk even when editing untrusted source code. Despite the widespread adoption of LSP, no existing techniques specifically target LSP server testing. To bridge this gap, we present LspFuzz, a grey-box hybrid fuzzer for systematic LSP server testing. Our key insight is that effective LSP server testing requires holistic mutation of source code and editor operations, as bugs often manifest from their combinations. To satisfy the sophisticated constraints of LSP and effectively explore the input space, we employ a two-stage mutation pipeline: syntax-aware mutations to source code, followed by context-aware dispatching of editor operations. We evaluated LspFuzz on four widely used LSP servers. LspFuzz demonstrated superior performance compared to baseline fuzzers, and uncovered previously unknown bugs in real-world LSP servers. Of the 51 bugs we reported, 42 have been confirmed, 26 have been fixed by developers, and two have been assigned CVE numbers. Our work advances the quality assurance of LSP servers, providing both a practical tool and foundational insights for future research in this domain.",
        "arxivUrl": "https://arxiv.org/abs/2510.00532",
        "paperUrl": "https://doi.org/10.1109/ASE63991.2025.00183",
        "bibtex": "@inproceedings{DBLP:conf/kbse/ZhuCTWLWC25,\n  author       = {Hengcheng Zhu and\n                  Songqiang Chen and\n                  Valerio Terragni and\n                  Lili Wei and\n                  Yepang Liu and\n                  Jiarong Wu and\n                  Shing{-}Chi Cheung},\n  title        = {LspFuzz: Hunting Bugs in Language Servers},\n  booktitle    = {40th {IEEE/ACM} International Conference on Automated Software Engineering,\n                  {ASE} 2025, Seoul, Korea, Republic of, November 16-20, 2025},\n  pages        = {2209--2221},\n  publisher    = {{IEEE}},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/ASE63991.2025.00183},\n  doi          = {10.1109/ASE63991.2025.00183},\n  timestamp    = {Sun, 08 Feb 2026 15:06:01 +0100},\n  biburl       = {https://dblp.org/rec/conf/kbse/ZhuCTWLWC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Managing Software Supply Chains - Theory and Practice.",
        "date": "2025-01-01",
        "authors": [
            "Ying Wang",
            "Shing-Chi Cheung",
            "Hai Yu",
            "Zhiliang Zhu"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "This book offers a comprehensive literature review on software supply chains, studies on dependency hell issues, and a toolkit and datasets to combat them",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1007/978-981-96-1797-5",
        "bibtex": "@book{DBLP:books/sp/WangCYZ25,\n  author       = {Ying Wang and\n                  Shing{-}Chi Cheung and\n                  Hai Yu and\n                  Zhiliang Zhu},\n  title        = {Managing Software Supply Chains - Theory and Practice},\n  publisher    = {Springer},\n  year         = {2025},\n  url          = {https://doi.org/10.1007/978-981-96-1797-5},\n  doi          = {10.1007/978-981-96-1797-5},\n  isbn         = {978-981-96-1796-8},\n  timestamp    = {Wed, 09 Apr 2025 09:19:47 +0200},\n  biburl       = {https://dblp.org/rec/books/sp/WangCYZ25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "A study on prompt design, advantages and limitations of ChatGPT for deep learning program repair.",
        "date": "2025-05-01",
        "authors": [
            "Jialun Cao",
            "Meiziniu Li",
            "Ming Wen",
            "Shing-Chi Cheung"
        ],
        "venue": "Automated Software Engineering",
        "venueShort": "Autom. Softw. Eng.",
        "abstract": "The emergence of large language models (LLMs) such as ChatGPT has revolutionized many fields. In particular, recent advances in LLMs have triggered various studies examining the use of these models for software development tasks, such as program repair, code understanding, and code generation. Prior studies have shown the capability of ChatGPT in repairing conventional programs. However, debugging deep learning (DL) programs poses unique challenges since the decision logic is not directly encoded in the source code. This requires LLMs to not only parse the source code syntactically but also understand the intention of DL programs. Therefore, ChatGPT’s capability in repairing DL programs remains unknown. To fill this gap, our study aims to answer three research questions: (1) Can ChatGPT debug DL programs effectively? (2) How can ChatGPT’s repair performance be improved by prompting? (3) In which way can dialogue help facilitate the repair? Our study analyzes the typical information that is useful for prompt design and suggests enhanced prompt templates that are more efficient for repairing DL programs. On top of them, we summarize the dual perspectives (i.e., advantages and disadvantages) of ChatGPT’s ability, such as its handling of API misuse and recommendation, and its shortcomings in identifying default parameters. Our findings indicate that ChatGPT has the potential to repair DL programs effectively and that prompt engineering and dialogue can further improve its performance by providing more code intention. We also identified the key intentions that can enhance ChatGPT’s program repairing capability.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1007/s10515-025-00492-x",
        "bibtex": "@article{DBLP:journals/ase/CaoLWC25,\n  author       = {Jialun Cao and\n                  Meiziniu Li and\n                  Ming Wen and\n                  Shing{-}Chi Cheung},\n  title        = {A study on prompt design, advantages and limitations of ChatGPT for\n                  deep learning program repair},\n  journal      = {Autom. Softw. Eng.},\n  volume       = {32},\n  number       = {1},\n  pages        = {30},\n  year         = {2025},\n  url          = {https://doi.org/10.1007/s10515-025-00492-x},\n  doi          = {10.1007/S10515-025-00492-X},\n  timestamp    = {Sun, 15 Jun 2025 21:07:19 +0200},\n  biburl       = {https://dblp.org/rec/journals/ase/CaoLWC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "How far are app secrets from being stolen? a case study on android.",
        "date": "2025-01-14",
        "authors": [
            "Lili Wei",
            "Heqing Huang",
            "Shing-Chi Cheung",
            "Kevin Li"
        ],
        "venue": "Empirical Software Engineering",
        "venueShort": "Empir. Softw. Eng.",
        "abstract": "Android apps can hold secret strings of themselves such as cloud service credentials or encryption keys. Leakage of such secret strings can induce unprecedented consequences like monetary losses or leakage of user private information. In practice, various security issues were reported because many apps failed to protect their secrets. However, little is known about the types, usages, exploitability, and consequences of app secret leakage issues. While a large body of literature has been devoted to studying user private information leakage, there is no systematic study characterizing app secret leakage issues. How far are Android app secrets from being stolen? To bridge this gap, we conducted the first systematic study to characterize app secret leakage issues in Android apps based on 575 potential app secrets sampled from 14,665 popular Android apps on Google Play. We summarized the common categories of leaked app secrets, assessed their security impacts and disclosed app bad practices in storing app secrets. We devised a text mining strategy using regular expressions and demonstrated that numerous app secrets can be easily stolen, even from the highly popular Android apps on Google. In a follow-up study, we harvested 3,711 distinct exploitable app secrets through automatic analysis. Our findings highlight the prevalence of this problem and call for greater attention to app secret protection.",
        "arxivUrl": "https://arxiv.org/abs/2501.07805",
        "paperUrl": "https://doi.org/10.1007/s10664-024-10607-9",
        "bibtex": "@article{DBLP:journals/corr/abs-2501-07805,\n  author       = {Lili Wei and\n                  Heqing Huang and\n                  Shing{-}Chi Cheung and\n                  Kevin Li},\n  title        = {How Far are App Secrets from Being Stolen? {A} Case Study on Android},\n  journal      = {CoRR},\n  volume       = {abs/2501.07805},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2501.07805},\n  doi          = {10.48550/ARXIV.2501.07805},\n  eprinttype    = {arXiv},\n  eprint       = {2501.07805},\n  timestamp    = {Fri, 16 May 2025 13:09:33 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2501-07805.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "On state reverting in solidity smart contracts: Developer practices, fault categorization, and tool evaluation.",
        "date": "2025-09-01",
        "authors": [
            "Lu Liu",
            "Lili Wei",
            "Wuqi Zhang",
            "Shuqing Li",
            "Yifan Zhou",
            "Yepang Liu",
            "Shing-Chi Cheung",
            "Michael R. Lyu"
        ],
        "venue": "Empirical Software Engineering",
        "venueShort": "Empir. Softw. Eng.",
        "abstract": "Smart contracts are computer programs deployed on blockchains to facilitate transactions. A critical aspect of smart contract security is the use of state-reverting statements (e.g., require, if...revert, if...throw). These statements protect transactions from abnormal behaviors or malicious attacks by reverting a contract to its previous state when certain input constraints or security properties are violated. While essential, the correct use of these state-reverting (SR) statements is nontrivial. Improper use can lead to security vulnerabilities, resulting in substantial financial losses or other severe consequences. It is, therefore, highly important to understand developers’ practices of state reverting in smart contracts and the common mistakes they make. To achieve this goal, we conduct the first comprehensive empirical study on the use of SR statements and their related faults in Solidity smart contracts. First, we analyze the prevalence and purposes of SR statements in 21,414 verified contracts from popular decentralized applications (dapps) and manually examine 381 SR statements, leading to a taxonomy of their uses. Second, we collect 320 real-world state-reverting faults (SR faults) from open-source projects on GitHub and audit reports on Code4rena. We categorize the SR faults into 17 types and summarize 12 distinct fixing strategies. This knowledge can help researchers and practitioners to better understand the common usages of SR statements and learn how to prevent or cope with SR faults. Lastly, the variety of SR fault types and the presence of high-risk issues highlight the need for automated tools to identify and mitigate these faults. This further motivates us to assess the SR fault detection performance of state-of-the-art security analyzers, with the aim of understanding their capability and identifying their deficiencies. Via evaluating 12 representative tools on a benchmark comprising 243 contracts with six types of SR faults and the corresponding patched versions, we observe that existing tools exhibit limited capabilities in detecting SR faults (the average detection rate is 14.4%). This result underscores the need for more advanced security analysis tools specifically tailored for SR faults. To facilitate the development of such tools, we further provide a comprehensive analysis of three common limitations of existing tools.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1007/s10664-025-10685-3",
        "bibtex": "@article{DBLP:journals/ese/LiuWZLZLCL25,\n  author       = {Lu Liu and\n                  Lili Wei and\n                  Wuqi Zhang and\n                  Shuqing Li and\n                  Yifan Zhou and\n                  Yepang Liu and\n                  Shing{-}Chi Cheung and\n                  Michael R. Lyu},\n  title        = {On state reverting in solidity smart contracts: Developer practices,\n                  fault categorization, and tool evaluation},\n  journal      = {Empir. Softw. Eng.},\n  volume       = {30},\n  number       = {5},\n  pages        = {141},\n  year         = {2025},\n  url          = {https://doi.org/10.1007/s10664-025-10685-3},\n  doi          = {10.1007/S10664-025-10685-3},\n  timestamp    = {Tue, 05 Aug 2025 22:47:17 +0200},\n  biburl       = {https://dblp.org/rec/journals/ese/LiuWZLZLCL25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Understanding and Characterizing Mock Assertions in Unit Tests.",
        "date": "2025-03-25",
        "authors": [
            "Hengcheng Zhu",
            "Valerio Terragni",
            "Lili Wei",
            "Shing-Chi Cheung",
            "Jiarong Wu",
            "Yepang Liu"
        ],
        "venue": "Proceedings of the ACM on Software Engineering",
        "venueShort": "Proc. ACM",
        "abstract": "Mock assertions provide developers with a powerful means to validate program behaviors that are unobservable to test assertions. Despite their significance, they are rarely considered by automated test generation techniques. Effective generation of mock assertions requires understanding how they are used in practice. Although previous studies highlighted the importance of mock assertions, none provide insight into their usages. To bridge this gap, we conducted the first empirical study on mock assertions, examining their adoption, the characteristics of the verified method invocations, and their effectiveness in fault detection. Our analysis of 4,652 test cases from 11 popular Java projects reveals that mock assertions are mostly applied to validating specific kinds of method calls, such as those interacting with external resources and those reflecting whether a certain code path was traversed in systems under test. Additionally, we find that mock assertions complement traditional test assertions by ensuring the desired side effects have been produced, validating control flow logic, and checking internal computation results. Our findings contribute to a better understanding of mock assertion usages and provide a foundation for future related research such as automated test generation that support mock assertions.",
        "arxivUrl": "https://arxiv.org/abs/2503.19284",
        "paperUrl": "https://doi.org/10.48550/arXiv.2503.19284",
        "bibtex": "@article{DBLP:journals/corr/abs-2503-19284,\n  author       = {Hengcheng Zhu and\n                  Valerio Terragni and\n                  Lili Wei and\n                  Shing{-}Chi Cheung and\n                  Jiarong Wu and\n                  Yepang Liu},\n  title        = {Understanding and Characterizing Mock Assertions in Unit Tests},\n  journal      = {CoRR},\n  volume       = {abs/2503.19284},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2503.19284},\n  doi          = {10.48550/ARXIV.2503.19284},\n  eprinttype    = {arXiv},\n  eprint       = {2503.19284},\n  timestamp    = {Fri, 16 May 2025 13:09:34 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2503-19284.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "SemBIC: Semantic-Aware Identification of Bug-Inducing Commits.",
        "date": "2025",
        "authors": [
            "Xiao Chen",
            "Hengcheng Zhu",
            "Jialun Cao",
            "Ming Wen",
            "Shing-Chi Cheung"
        ],
        "venue": "Proceedings of the ACM on Software Engineering",
        "venueShort": "Proc. ACM",
        "abstract": "",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1145/3715781",
        "bibtex": "@article{DBLP:journals/pacmse/ChenZCWC25,\n  author       = {Xiao Chen and\n                  Hengcheng Zhu and\n                  Jialun Cao and\n                  Ming Wen and\n                  Shing{-}Chi Cheung},\n  title        = {SemBIC: Semantic-Aware Identification of Bug-Inducing Commits},\n  journal      = {Proc. {ACM} Softw. Eng.},\n  volume       = {2},\n  number       = {{FSE}},\n  pages        = {1363--1385},\n  year         = {2025},\n  url          = {https://doi.org/10.1145/3715781},\n  doi          = {10.1145/3715781},\n  timestamp    = {Thu, 11 Sep 2025 20:25:21 +0200},\n  biburl       = {https://dblp.org/rec/journals/pacmse/ChenZCWC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "An Empirical Study of Bugs in Data Visualization Libraries.",
        "date": "2025-01-01",
        "authors": [
            "Weiqi Lu",
            "Yongqiang Tian",
            "Xiaohan Zhong",
            "Haoyang Ma",
            "Zhenyang Xu",
            "Shing-Chi Cheung",
            "Chengnian Sun"
        ],
        "venue": "Proceedings of the ACM on Software Engineering",
        "venueShort": "Proc. ACM",
        "abstract": "Data visualization (DataViz) libraries play a crucial role in presentation, data analysis, and application development, underscoring the importance of their accuracy in transforming data into visual representations. Incorrect visualizations can adversely impact user experience, distort information conveyance, and influence user perception and decision-making processes. Visual bugs in these libraries can be particularly insidious as they may not cause obvious errors like crashes, but instead mislead users of the underlying data graphically, resulting in wrong decision making. Consequently, a good understanding of the unique characteristics of bugs in DataViz libraries is essential for researchers and developers to detect and fix bugs in DataViz libraries. This study presents the first comprehensive analysis of bugs in DataViz libraries, examining 564 bugs collected from five widely-used libraries. Our study systematically analyzes their symptoms and root causes, and provides a detailed taxonomy. We found that incorrect/inaccurate plots are pervasive in DataViz libraries and incorrect graphic computation is the major root cause, which necessitates further automated testing methods for DataViz libraries. Moreover, we identified eight key steps to trigger such bugs and two test oracles specific to DataViz libraries, which may inspire future research in designing effective automated testing techniques. Furthermore, with the recent advancements in Vision Language Models (VLMs), we explored the feasibility of applying these models to detect incorrect/inaccurate plots. The results show that the effectiveness of VLMs in bug detection varies from 29% to 57%, depending on the prompts, and adding more information in prompts does not necessarily increase the effectiveness. More findings can be found in our manuscript.",
        "arxivUrl": "https://arxiv.org/abs/2506.15084",
        "paperUrl": "https://doi.org/10.48550/arXiv.2506.15084",
        "bibtex": "@article{DBLP:journals/corr/abs-2506-15084,\n  author       = {Weiqi Lu and\n                  Yongqiang Tian and\n                  Xiaohan Zhong and\n                  Haoyang Ma and\n                  Zhenyang Xu and\n                  Shing{-}Chi Cheung and\n                  Chengnian Sun},\n  title        = {An Empirical Study of Bugs in Data Visualization Libraries},\n  journal      = {CoRR},\n  volume       = {abs/2506.15084},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2506.15084},\n  doi          = {10.48550/ARXIV.2506.15084},\n  eprinttype    = {arXiv},\n  eprint       = {2506.15084},\n  timestamp    = {Fri, 11 Jul 2025 12:55:00 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2506-15084.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Question Selection for Multimodal Code Search Synthesis Using Probabilistic Version Spaces.",
        "date": "2025-01-01",
        "authors": [
            "Jiarong Wu",
            "Yanyan Jiang",
            "Lili Wei",
            "Congying Xu",
            "Shing-Chi Cheung",
            "Chang Xu"
        ],
        "venue": "IEEE Transactions on Software Engineering",
        "venueShort": "IEEE",
        "abstract": "Searching the occurrences of specific code patterns (code search) is a common task in software engineering, and programming by example (PBE) techniques have been applied to ease customizing code patterns. However, previous PBE tools only synthesize programs meeting the input-output examples, which may not always align with the user intent. To bridge this gap, this paper proposes <sc xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">Excalibur</small>, a multi-modal (example and natural language description) and interactive synthesizer for code search. <sc xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">Excalibur</small> ensures that the generated programs are correct for the provided examples (soundness) and include the user-intended program (bounded completeness). Furthermore, <sc xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">Excalibur</small> helps the user identify the user-intended program through question-answer interaction. To minimize the required interaction efforts, question selection is crucial. To improve question selection for code search, we propose probabilistic version spaces (ProbVS), in which the user-intended program’s probability is high and others are low. ProbVS combines traditional version spaces for compactly representing extensive programs and large language models (on the user-provided natural language description) for adjusting programs’ probabilities to align with users’ intents. Extensive experiments on a benchmark of 44 tasks demonstrated the effectiveness of <sc xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">Excalibur</small> and ProbVS and demystified how ProbVS affects probability distributions and how the configurable parameters affect ProbVS.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1109/TSE.2025.3565387",
        "bibtex": "@article{DBLP:journals/tse/WuJWXCX25,\n  author       = {Jiarong Wu and\n                  Yanyan Jiang and\n                  Lili Wei and\n                  Congying Xu and\n                  Shing{-}Chi Cheung and\n                  Chang Xu},\n  title        = {Question Selection for Multimodal Code Search Synthesis Using Probabilistic\n                  Version Spaces},\n  journal      = {{IEEE} Trans. Software Eng.},\n  volume       = {51},\n  number       = {6},\n  pages        = {1724--1744},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/TSE.2025.3565387},\n  doi          = {10.1109/TSE.2025.3565387},\n  timestamp    = {Sun, 06 Jul 2025 13:22:55 +0200},\n  biburl       = {https://dblp.org/rec/journals/tse/WuJWXCX25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "DOMAINEVAL: An Auto-Constructed Benchmark for Multi-Domain Code Generation.",
        "date": "2025-04-11",
        "authors": [
            "Qiming Zhu",
            "Jialun Cao",
            "Yaojie Lu",
            "Hongyu Lin",
            "Xianpei Han",
            "Le Sun",
            "Shing-Chi Cheung"
        ],
        "venue": "AAAI-25",
        "venueShort": "USA",
        "abstract": "Code benchmarks such as HumanEval are widely adopted to evaluate the capabilities of Large Language Models (LLMs), providing insights into their strengths and weaknesses. However, current benchmarks primarily exercise LLMs' capability on common coding tasks (e.g., bubble sort, greatest common divisor), leaving domain-specific coding tasks (e.g., computation, system, cryptography) unexplored. To fill this gap, we propose a multi-domain code benchmark, DOMAINEVAL, designed to evaluate LLMs' coding capabilities thoroughly. Our pipeline works in a fully automated manner, enabling a push-button construction from code repositories into formatted subjects under study. Interesting findings are observed by evaluating 12 representative LLMs against DOMAINEVAL. We notice that LLMs are generally good at computation tasks while falling short on cryptography and system coding tasks. The performance gap can be as much as 68.94% (80.94% - 12.0%) in some LLMs. We also observe that generating more samples can increase the overall performance of LLMs, while the domain bias may even increase. The contributions of this study include a code generation benchmark dataset DOMAINEVAL, encompassing six popular domains, a fully automated pipeline for constructing code benchmarks, and an identification of the limitations of LLMs in code generation tasks based on their performance on DOMAINEVAL, providing directions for future research improvements.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1609/aaai.v39i24.34811",
        "bibtex": "@inproceedings{DBLP:conf/aaai/ZhuC0LH0C25,\n  author       = {Qiming Zhu and\n                  Jialun Cao and\n                  Yaojie Lu and\n                  Hongyu Lin and\n                  Xianpei Han and\n                  Le Sun and\n                  Shing{-}Chi Cheung},\n  editor       = {Toby Walsh and\n                  Julie Shah and\n                  Zico Kolter},\n  title        = {{DOMAINEVAL:} An Auto-Constructed Benchmark for Multi-Domain Code\n                  Generation},\n  booktitle    = {AAAI-25, Sponsored by the Association for the Advancement of Artificial\n                  Intelligence, February 25 - March 4, 2025, Philadelphia, PA, {USA}},\n  pages        = {26148--26156},\n  publisher    = {{AAAI} Press},\n  year         = {2025},\n  url          = {https://doi.org/10.1609/aaai.v39i24.34811},\n  doi          = {10.1609/AAAI.V39I24.34811},\n  timestamp    = {Sun, 01 Feb 2026 13:23:21 +0100},\n  biburl       = {https://dblp.org/rec/conf/aaai/ZhuC0LH0C25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "CRUXEVAL-X: A Benchmark for Multilingual Code Reasoning, Understanding and Execution.",
        "date": "2025",
        "authors": [
            "Ruiyang Xu",
            "Jialun Cao",
            "Yaojie Lu",
            "Ming Wen",
            "Hongyu Lin",
            "Xianpei Han",
            "Ben He",
            "Shing-Chi Cheung",
            "Le Sun"
        ],
        "venue": "the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
        "venueShort": "ACL",
        "abstract": "Ruiyang Xu, Jialun Cao, Yaojie Lu, Ming Wen, Hongyu Lin, Xianpei Han, Ben He, Shing-Chi Cheung, Le Sun. Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2025.",
        "arxivUrl": "",
        "paperUrl": "https://aclanthology.org/2025.acl-long.1158/",
        "bibtex": "@inproceedings{DBLP:conf/acl/XuC00LHHC025,\n  author       = {Ruiyang Xu and\n                  Jialun Cao and\n                  Yaojie Lu and\n                  Ming Wen and\n                  Hongyu Lin and\n                  Xianpei Han and\n                  Ben He and\n                  Shing{-}Chi Cheung and\n                  Le Sun},\n  editor       = {Wanxiang Che and\n                  Joyce Nabende and\n                  Ekaterina Shutova and\n                  Mohammad Taher Pilehvar},\n  title        = {{CRUXEVAL-X:} {A} Benchmark for Multilingual Code Reasoning, Understanding\n                  and Execution},\n  booktitle    = {Proceedings of the 63rd Annual Meeting of the Association for Computational\n                  Linguistics (Volume 1: Long Papers), {ACL} 2025, Vienna, Austria,\n                  July 27 - August 1, 2025},\n  pages        = {23762--23779},\n  publisher    = {Association for Computational Linguistics},\n  year         = {2025},\n  url          = {https://aclanthology.org/2025.acl-long.1158/},\n  timestamp    = {Sun, 02 Nov 2025 21:27:24 +0100},\n  biburl       = {https://dblp.org/rec/conf/acl/XuC00LHHC025.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "From Informal to Formal - Incorporating and Evaluating LLMs on Natural Language Requirements to Verifiable Formal Proofs.",
        "date": "2025-01-27",
        "authors": [
            "Jialun Cao",
            "Yaojie Lu",
            "Meiziniu Li",
            "Haoyang Ma",
            "Haokun Li",
            "Mengda He",
            "Cheng Wen",
            "Le Sun",
            "Hongyu Zhang",
            "Shengchao Qin",
            "Shing-Chi Cheung",
            "Cong Tian"
        ],
        "venue": "the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
        "venueShort": "ACL",
        "abstract": "The research in AI-based formal mathematical reasoning has shown an unstoppable growth trend. These studies have excelled in mathematical competitions like IMO and have made significant progress. This paper focuses on formal verification, an immediate application scenario of formal reasoning, and breaks it down into sub-tasks. We constructed 18k high-quality instruction-response pairs across five formal specification languages (Coq, Lean4, Dafny, ACSL, and TLA+) by distilling gpt-4o and evaluated against ten open-sourced LLMs, including recent popular DeepSeek-R1. We also fine-tuned several 7~8B small models to achieve comparable performance with Deepseek-R1-671B. Interestingly, we observed that fine-tuning with formal data also enhances mathematics, reasoning, and coding capabilities. Fine-tuned models are released at https: //huggingface.co/fm-universe.",
        "arxivUrl": "https://arxiv.org/abs/2501.16207",
        "paperUrl": "https://aclanthology.org/2025.acl-long.1310/",
        "bibtex": "@inproceedings{DBLP:conf/acl/Cao0LMLH000QCT25,\n  author       = {Jialun Cao and\n                  Yaojie Lu and\n                  Meiziniu Li and\n                  Haoyang Ma and\n                  Haokun Li and\n                  Mengda He and\n                  Cheng Wen and\n                  Le Sun and\n                  Hongyu Zhang and\n                  Shengchao Qin and\n                  Shing{-}Chi Cheung and\n                  Cong Tian},\n  editor       = {Wanxiang Che and\n                  Joyce Nabende and\n                  Ekaterina Shutova and\n                  Mohammad Taher Pilehvar},\n  title        = {From Informal to Formal - Incorporating and Evaluating LLMs on Natural\n                  Language Requirements to Verifiable Formal Proofs},\n  booktitle    = {Proceedings of the 63rd Annual Meeting of the Association for Computational\n                  Linguistics (Volume 1: Long Papers), {ACL} 2025, Vienna, Austria,\n                  July 27 - August 1, 2025},\n  pages        = {26984--27003},\n  publisher    = {Association for Computational Linguistics},\n  year         = {2025},\n  url          = {https://aclanthology.org/2025.acl-long.1310/},\n  timestamp    = {Sun, 02 Nov 2025 21:27:24 +0100},\n  biburl       = {https://dblp.org/rec/conf/acl/Cao0LMLH000QCT25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "A Tale of Two DL Cities: When Library Tests Meet Compiler.",
        "date": "2025-04-26",
        "authors": [
            "Qingchao Shen",
            "Yongqiang Tian",
            "Haoyang Ma",
            "Junjie Chen",
            "Lili Huang",
            "Ruifeng Fu",
            "Shing-Chi Cheung",
            "Zan Wang"
        ],
        "venue": "47th IEEE/ACM International Conference on Software Engineering",
        "venueShort": "ICSE",
        "abstract": "Deep Learning (DL) compilers typically load a DL model and optimize it with intermediate representation. Existing DL compiler testing techniques mainly focus on model optimization stages, but rarely explore bug detection at the model loading stage. Effectively testing the model loading stage requires covering diverse usages of each DL operator from various DL libraries, which shares a common objective with DL library testing, indicating that the embedded knowledge in DL library tests is beneficial for testing the model loading stage of DL compilers. With this idea, we propose Opera to migrate the knowledge embedded in DL library tests to test the model loading stage. Opera constructs diverse tests from various tests for DL libraries (including the tests documented in DL libraries and those generated by recent fuzzers). In total, we considered three sources of tests in DL libraries for migration. In addition, it incorporates a diversity-based test prioritization strategy to migrate and execute those tests that are more likely to detect diverse bugs earlier. We then used eight frontends from three DL compilers (e.g., TVM, TensorRT, and OpenVINO) for evaluation. OPERA detected 170 previously unknown bugs in total, 90 of which have been confirmed/fixed by developers, demonstrating the effectiveness of such the migration-based idea. The test prioritization strategy in OPERA improves testing efficiency with migrated tests by <tex xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">$11.9 \\% \\sim 47.4 \\%$</tex> on average compared to general test prioritization strategies.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1109/ICSE55347.2025.00025",
        "bibtex": "@inproceedings{DBLP:conf/icse/ShenTMCHFCW25,\n  author       = {Qingchao Shen and\n                  Yongqiang Tian and\n                  Haoyang Ma and\n                  Junjie Chen and\n                  Lili Huang and\n                  Ruifeng Fu and\n                  Shing{-}Chi Cheung and\n                  Zan Wang},\n  title        = {A Tale of Two {DL} Cities: When Library Tests Meet Compiler},\n  booktitle    = {47th {IEEE/ACM} International Conference on Software Engineering,\n                  {ICSE} 2025, Ottawa, ON, Canada, April 26 - May 6, 2025},\n  pages        = {2201--2212},\n  publisher    = {{IEEE}},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/ICSE55347.2025.00025},\n  doi          = {10.1109/ICSE55347.2025.00025},\n  timestamp    = {Fri, 04 Jul 2025 22:07:55 +0200},\n  biburl       = {https://dblp.org/rec/conf/icse/ShenTMCHFCW25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Differential Testing of Concurrent Classes.",
        "date": "2025-03-31",
        "authors": [
            "Valerio Terragni",
            "Shing-Chi Cheung"
        ],
        "venue": "IEEE Conference on Software Testing",
        "venueShort": "ICST",
        "abstract": "Concurrent programs are pervasive, yet difficult to write. The inherent complexity of thread synchronization makes the evolution of concurrent programs prone to concurrency faults. Previous work on regression testing concurrent programs focused on reducing the cost of re-run the existing tests. However, existing tests may not be able to expose the regression faults in the modified program. In this paper, we present Condiff a differential testing technique that generates concurrent tests and oracles to expose behavioral differences between two versions of a given concurrent class. Since concurrent programs are non-deterministic, this involves exploring all possible non-deterministic thread interleavings of each generated test on both versions. However, we can afford to analyze only a few concurrent tests due to the high cost of exhaustive interleaving exploration. To address the challenge, Condiff leverages the information of code changes and trace analysis to analyze only those concurrent tests that are likely to expose behavioral differences (if they exist). We evaluated Condiff on a set of Java classes. Our results show that Condiff can effectively generate concurrent tests that expose behavioral differences.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1109/ICST62969.2025.10989027",
        "bibtex": "@inproceedings{DBLP:conf/icst/TerragniC25,\n  author       = {Valerio Terragni and\n                  Shing{-}Chi Cheung},\n  title        = {Differential Testing of Concurrent Classes},\n  booktitle    = {{IEEE} Conference on Software Testing, Verification and Validation,\n                  {ICST} 2025, Napoli, Italy, March 31 - April 4, 2025},\n  pages        = {255--266},\n  publisher    = {{IEEE}},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/ICST62969.2025.10989027},\n  doi          = {10.1109/ICST62969.2025.10989027},\n  timestamp    = {Fri, 30 May 2025 12:23:35 +0200},\n  biburl       = {https://dblp.org/rec/conf/icst/TerragniC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Cross2OH: Enabling Seamless Porting of C/C++ Software Libraries to OpenHarmony.",
        "date": "2025-11-16",
        "authors": [
            "Qian Zhang",
            "Tsz-On Li",
            "Ying Wang",
            "Li Li",
            "Shing-Chi Cheung"
        ],
        "venue": "40th IEEE/ACM International Conference on Automated Software Engineering",
        "venueShort": "ASE",
        "abstract": "OpenHarmony is a new mobile operating system that offers a popular alternative to Android and iOS. To support its adoption, significant efforts have been devoted to porting C/C++ libraries from Linux to OpenHarmony. However, this porting process presents unique challenges due to the fundamental architectural differences in system libraries, runtime environments, and build systems between the two platforms. These discrepancies manifest as Cross-platform Incompatibility (CPI) issues during cross-compilation, which are particularly difficult to resolve for two key reasons. First, conventional cross-compilation toolchains provide only brief error messages that offer inadequate diagnostic information for CPI issues. Second, resolving these issues requires a deep understanding of cross-platform discrepancies, yet comprehensive documentation or systematic guidelines about such Linux-to-OpenHarmony differences remain largely unavailable.In this experience paper, to assist developers in addressing these challenges, we conducted an empirical study on 92 C/C++ libraries successfully ported to OpenHarmony. Through manual step-by-step reproduction of all CPI issues, our study reveals that discrepancies between Linux and OpenHarmony can be divided into three categories, and CPI issues can manifest through eight dimensions. Furthermore, we identified eight common adaptation strategies for resolving CPI issues. Based on these findings, we present Cross2OH, an automated technique for porting Linux-based software to OpenHarmony. Our approach combines: (1) an adaptation knowledge base (derived from RQ1 and RQ2 findings) and (2) a static analysis approach to detect and patch eight types of CPI issues. Evaluation using real developer patches shows Cross2OH achieves 0.94 recall and 0.91 precision in resolving CPI issues. Notably, Cross2OH enables successful cross-compilation for 40 critical libraries (including dependencies for popular Android apps such as WeChat, Microsoft Excel, Bilibili), with 29 of them passed official OpenHarmony review. The evaluation results demonstrate Cross2OH’s potential to streamline the porting process and foster the growth of the OpenHarmony software ecosystem.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1109/ASE63991.2025.00146",
        "bibtex": "@inproceedings{DBLP:conf/kbse/ZhangLWLC25,\n  author       = {Qian Zhang and\n                  Tsz{-}On Li and\n                  Ying Wang and\n                  Li Li and\n                  Shing{-}Chi Cheung},\n  title        = {Cross2OH: Enabling Seamless Porting of {C/C++} Software Libraries\n                  to OpenHarmony},\n  booktitle    = {40th {IEEE/ACM} International Conference on Automated Software Engineering,\n                  {ASE} 2025, Seoul, Korea, Republic of, November 16-20, 2025},\n  pages        = {1744--1755},\n  publisher    = {{IEEE}},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/ASE63991.2025.00146},\n  doi          = {10.1109/ASE63991.2025.00146},\n  timestamp    = {Tue, 10 Feb 2026 07:40:32 +0100},\n  biburl       = {https://dblp.org/rec/conf/kbse/ZhangLWLC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Demystifying Cross-Language C/C++ Binaries: A Robust Software Component Analysis Approach.",
        "date": "2025-11-16",
        "authors": [
            "Meiqiu Xu",
            "Ying Wang",
            "Wei Tang",
            "Xian Zhan",
            "Shing-Chi Cheung",
            "Hai Yu",
            "Zhiliang Zhu"
        ],
        "venue": "40th IEEE/ACM International Conference on Automated Software Engineering",
        "venueShort": "ASE",
        "abstract": "Binary Software Composition Analysis (BSCA) is a technique for identifying the versions of third-party libraries (TPLs) used in compiled binaries, thereby tracing the dependencies and vulnerabilities of software components without access to their source code. However, existing BSCA techniques struggle with cross-language invoked C/C++ binaries in polyglot projects due to two key challenges: (1) interference from heterogeneous Foreign Function Interface (FFI) bindings that obscure distinctive TPL features and generate false positives during matching processes, and (2) the inherent complexity of composite binaries (fused binaries), particularly prevalent in polyglot development where multiple TPLs are frequently compiled into single executable units, resulting in blurred boundaries between libraries and substantially compromising version identification precision.We propose DeeperBin, a BSCA technique that addresses these challenges through a high-quality, large-scale feature database with four key advantages: (1) high scalability that is capable of analyzing 74,647 C/C++ TPL versions, (2) efficient noise filtering to remove FFI bindings and common functions, (3) automated extraction of version string regexes for 31,855 TPL versions, and (4) generation of distinctive version features using the Minimum Description Length (MDL) principle. Evaluated on 418 cross-language binaries, DeeperBin achieves 81.2% precision and 84.6% recall for TPL detection, outperforming state-of-the-art (SOTA) techniques by 14.1% and 23.2%, respectively. For version identification, it achieves 70.3% precision, a 12.6% improvement over state-of-the-art techniques. Ablation studies confirm the usefulness of FFI filtering and MDL-based features, boosting precision and recall by 17.1% and 18.8%. DeeperBin also maintains competitive efficiency, processing binaries in 364.3 seconds while supporting the largest feature database.",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.1109/ASE63991.2025.00148",
        "bibtex": "@inproceedings{DBLP:conf/kbse/XuWTZCYZ25,\n  author       = {Meiqiu Xu and\n                  Ying Wang and\n                  Wei Tang and\n                  Xian Zhan and\n                  Shing{-}Chi Cheung and\n                  Hai Yu and\n                  Zhiliang Zhu},\n  title        = {Demystifying Cross-Language {C/C++} Binaries: {A} Robust Software\n                  Component Analysis Approach},\n  booktitle    = {40th {IEEE/ACM} International Conference on Automated Software Engineering,\n                  {ASE} 2025, Seoul, Korea, Republic of, November 16-20, 2025},\n  pages        = {1768--1780},\n  publisher    = {{IEEE}},\n  year         = {2025},\n  url          = {https://doi.org/10.1109/ASE63991.2025.00148},\n  doi          = {10.1109/ASE63991.2025.00148},\n  timestamp    = {Mon, 09 Feb 2026 07:52:23 +0100},\n  biburl       = {https://dblp.org/rec/conf/kbse/XuWTZCYZ25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Data of Differential Testing of Concurrent Classes - ICST 2025.",
        "date": "2025-01-23",
        "authors": [
            "Valerio Terragni",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "ConDiff Artifact - ICST 2025 Differential Testing of Concurrent Classes Valerio Terragni University of Auckland, New Zealand v.terragni@auckland.ac.nzhttps://valerio-terragni.github.io/ Shing-Chi Cheung The Hong Kong University of Science and Technology, Hong Kong Accepted at ICST 2025 @inproceedings{Terragni2025ConDiff, author = {Valerio Terragni and Shing-Chi Cheung}, title = {Differential Testing of Concurrent Classes}, booktitle = {The 18th IEEE International Conference on Software Testing, Verification and Validation (ICST)}, year = {2025}, publisher = {IEEE},} Subjects and Results Folders Overview The following folders contain all the program revisions used in our experiments: - benchmarksC-B - benchmarksC-BR100 - benchmarksC-BR50 - benchmarksC-BR25 Each folder includes two program versions: - V1: The version without the fault. - V2: The faulty version. Results Folder The `results` folder contains the outputs of ConDiff and the Baseline. The files are organized as follows: - Files starting with `true_`: Results of ConDiff with the filtering phase enabled. - Files starting with `false_`: Results of the Baseline, i.e., the variant of ConDiff without the filtering phase enabled. Each file includes the results of 10 runs for each subject. --- Results Details The results include the detected behavioral differences (if any) and the following metrics (all time measurements are in milliseconds): - SR: Success Rate - DRT: Difference Revealing Time - CT: Number of concurrent tests generated - CTB: Number of concurrent tests analyzed by the behavioral checker - CTPRUNED: Number of pruned tests - PREFIXPRUNED: Number of pruned prefixes that lead to sequential behavioral differences - SUFFIXPRUNED: Number of pruned suffixes that lead to sequential behavioral differences - CFP: Number of concurrent function pairs containing at least one changed method Time Measurements - TIME_SCHANGE: Time to identify methods that are changed across revisions - TIME_GEN: Time to generate the tests - TIME_DIFFSEQ: Time for sequential behavioral checking - TIME_DIFFCON: Time for concurrent behavioral checking - TIME_CIA: Time for change impact analysis",
        "arxivUrl": "",
        "paperUrl": "https://doi.org/10.5281/zenodo.14722293",
        "bibtex": "@misc{DBLP:data/11/TerragniC25,\n  author       = {Valerio Terragni and\n                  Shing{-}Chi Cheung},\n  title        = {Data of Differential Testing of Concurrent Classes - {ICST} 2025 (Version\n                  1)},\n  publisher    = {Zenodo},\n  year         = {2025},\n  month        = jan,\n  howpublished = {\\url{https://doi.org/10.5281/zenodo.14722293}},\n  note         = {Accessed on YYYY-MM-DD.},\n  url          = {https://doi.org/10.5281/zenodo.14722293},\n  doi          = {10.5281/ZENODO.14722293},\n  timestamp    = {Tue, 19 Aug 2025 15:51:37 +0200},\n  biburl       = {https://dblp.org/rec/data/11/TerragniC25.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "How Should I Build A Benchmark? Revisiting Code-Related Benchmarks For LLMs.",
        "date": "2025-01-18",
        "authors": [
            "Jialun Cao",
            "Yuk-Kit Chan",
            "Zixuan Ling",
            "Wenxuan Wang",
            "Shuqing Li",
            "Mingwei Liu",
            "Ruixi Qiao",
            "Yuting Han",
            "Chaozheng Wang",
            "Boxi Yu",
            "Pinjia He",
            "Shuai Wang",
            "Zibin Zheng",
            "Michael R. Lyu",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Code-related benchmarks play a critical role in evaluating large language models (LLMs), yet their quality fundamentally shapes how the community interprets model capabilities. In the past few years, awareness of benchmark quality has grown. Yet, after a decade-scale (2014-2025) survey over 572 code benchmarks, we observed a lag between growing awareness and actual practice. For example, in 2025 alone, the number of benchmarks that ignore code coverage when providing test cases nearly matches the total count accumulated across the previous ten years. In response, we take a clear position: Code benchmarks must prioritize rigor in benchmark construction, reliability in evaluation, and reproducibility in release. To operationalize this position, we introduce a code benchmark guideline HOW2BENCH with 55 checklists. Finally, our further human study also exposed that the current issues not only stem from the significant effort required, but also from a lack of awareness regarding their importance.",
        "arxivUrl": "https://arxiv.org/abs/2501.10711",
        "paperUrl": "https://doi.org/10.48550/arXiv.2501.10711",
        "bibtex": "@article{DBLP:journals/corr/abs-2501-10711,\n  author       = {Jialun Cao and\n                  Yuk{-}Kit Chan and\n                  Zixuan Ling and\n                  Wenxuan Wang and\n                  Shuqing Li and\n                  Mingwei Liu and\n                  Ruixi Qiao and\n                  Yuting Han and\n                  Chaozheng Wang and\n                  Boxi Yu and\n                  Pinjia He and\n                  Shuai Wang and\n                  Zibin Zheng and\n                  Michael R. Lyu and\n                  Shing{-}Chi Cheung},\n  title        = {How Should {I} Build {A} Benchmark? Revisiting Code-Related Benchmarks\n                  For LLMs},\n  journal      = {CoRR},\n  volume       = {abs/2501.10711},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2501.10711},\n  doi          = {10.48550/ARXIV.2501.10711},\n  eprinttype    = {arXiv},\n  eprint       = {2501.10711},\n  timestamp    = {Sat, 17 May 2025 12:25:01 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2501-10711.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Isolating Language-Coding from Problem-Solving: Benchmarking LLMs with PseudoEval.",
        "date": "2025-02-26",
        "authors": [
            "Jiarong Wu",
            "Songqiang Chen",
            "Jialun Cao",
            "Hau Ching Lo",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Existing code generation benchmarks for Large Language Models (LLMs) such as HumanEval and MBPP are designed to study LLMs' end-to-end performance, where the benchmarks feed a problem description in natural language as input and examine the generated code in specific programming languages. However, the evaluation scores revealed in this way provide a little hint as to the bottleneck of the code generation -- whether LLMs are struggling with their problem-solving capability or language-coding capability. To answer this question, we construct PseudoEval, a multilingual code generation benchmark that provides a solution written in pseudocode as input. By doing so, the bottleneck of code generation in various programming languages could be isolated and identified. Our study yields several interesting findings. For example, we identify that the bottleneck of LLMs in Python programming is problem-solving, while Rust is struggling relatively more in language-coding. Also, our study indicates that problem-solving capability may transfer across programming languages, while language-coding needs more language-specific effort, especially for undertrained programming languages. Finally, we release the pipeline of constructing PseudoEval to facilitate the extension to existing benchmarks. PseudoEval is available at: this https URL .",
        "arxivUrl": "https://arxiv.org/abs/2502.19149",
        "paperUrl": "https://doi.org/10.48550/arXiv.2502.19149",
        "bibtex": "@article{DBLP:journals/corr/abs-2502-19149,\n  author       = {Jiarong Wu and\n                  Songqiang Chen and\n                  Jialun Cao and\n                  Hau Ching Lo and\n                  Shing{-}Chi Cheung},\n  title        = {Isolating Language-Coding from Problem-Solving: Benchmarking LLMs\n                  with PseudoEval},\n  journal      = {CoRR},\n  volume       = {abs/2502.19149},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2502.19149},\n  doi          = {10.48550/ARXIV.2502.19149},\n  eprinttype    = {arXiv},\n  eprint       = {2502.19149},\n  timestamp    = {Thu, 20 Mar 2025 21:38:11 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2502-19149.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "When LLMs Meet API Documentation: Can Retrieval Augmentation Aid Code Generation Just as It Helps Developers?",
        "date": "2025-03-19",
        "authors": [
            "Jingyi Chen",
            "Songqiang Chen",
            "Jialun Cao",
            "Jiasi Shen",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Retrieval-augmented generation (RAG) has increasingly shown its power in extending large language models' (LLMs') capability beyond their pre-trained knowledge. Existing works have shown that RAG can help with software development tasks such as code generation, code update, and test generation. Yet, the effectiveness of adapting LLMs to fast-evolving or less common API libraries using RAG remains unknown. To bridge this gap, we take an initial step to study this unexplored yet practical setting - when developers code with a less common library, they often refer to its API documentation; likewise, when LLMs are allowed to look up API documentation via RAG, to what extent can LLMs be advanced? To mimic such a setting, we select four less common open-source Python libraries with a total of 1017 eligible APIs. We study the factors that affect the effectiveness of using the documentation of less common API libraries as additional knowledge for retrieval and generation. Our intensive study yields interesting findings: (1) RAG helps improve LLMs' performance by 83%-220%. (2) Example code contributes the most to advance LLMs, instead of the descriptive texts and parameter lists in the API documentation. (3) LLMs could sometimes tolerate mild noises (typos in description or incorrect parameters) by referencing their pre-trained knowledge or document context. Finally, we suggest that developers pay more attention to the quality and diversity of the code examples in the API documentation. The study sheds light on future low-code software development workflows.",
        "arxivUrl": "https://arxiv.org/abs/2503.15231",
        "paperUrl": "https://doi.org/10.48550/arXiv.2503.15231",
        "bibtex": "@article{DBLP:journals/corr/abs-2503-15231,\n  author       = {Jingyi Chen and\n                  Songqiang Chen and\n                  Jialun Cao and\n                  Jiasi Shen and\n                  Shing{-}Chi Cheung},\n  title        = {When LLMs Meet {API} Documentation: Can Retrieval Augmentation Aid\n                  Code Generation Just as It Helps Developers?},\n  journal      = {CoRR},\n  volume       = {abs/2503.15231},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2503.15231},\n  doi          = {10.48550/ARXIV.2503.15231},\n  eprinttype    = {arXiv},\n  eprint       = {2503.15231},\n  timestamp    = {Wed, 30 Apr 2025 15:11:25 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2503-15231.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Bounded Exhaustive Random Program Generation for Testing Solidity Compilers and Analyzers.",
        "date": "2025-03-26",
        "authors": [
            "Haoyang Ma",
            "Alastair F. Donaldson",
            "Qingchao Shen",
            "Yongqiang Tian",
            "Junjie Chen",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "By July 2025, smart contracts collectively manage roughly $120 billion in assets. With Solidity remaining the dominant language for smart contract development, the correctness of Solidity compilers has become critically important. However, Solidity compilers are bug-prone, with a recent study revealing that combinations of qualifiers in Solidity programs are the primary cause of compiler crashes, accounting for 40.5% of all historical crashes. While random program generators are widely used for compiler testing, they may be less effective at finding Solidity compiler bugs because they explore the unbounded space of possible programs rather than concentrating on the specific subspace related to bug-prone qualifiers. A promising idea for finding qualifier-related bugs is to bound the search space based on empirical evidence of where such bugs are likely to occur, specifically focusing test generation to target subspaces with rich combinations of qualifiers. To address this, we propose bounded exhaustive random program generation, a novel approach that dynamically bounds the search space, enhancing the likelihood of uncovering Solidity compiler bugs. Specifically, our method bounds the search space by generating valid program templates that abstract programs that use bug-prone qualifiers, and then uses these templates as a basis for compiler testing through exhaustive enumeration of suitable qualifiers. Mechanisms are devised to address technical challenges regarding validity and efficiency. We have implemented our novel generation approach in a new tool, Erwin. We have used Erwin to find and report 26 bugs across two Solidity compilers, solc and solang, and one Solidity static analyzer, slither. Among these, 23 were previously unknown, 18 have been confirmed, and 10 have been fixed. Evaluation results demonstrate that Erwin outperforms state-of-the-art Solidity fuzzers in bug detection.",
        "arxivUrl": "https://arxiv.org/abs/2503.20332",
        "paperUrl": "https://doi.org/10.48550/arXiv.2503.20332",
        "bibtex": "@article{DBLP:journals/corr/abs-2503-20332,\n  author       = {Haoyang Ma and\n                  Alastair F. Donaldson and\n                  Qingchao Shen and\n                  Yongqiang Tian and\n                  Junjie Chen and\n                  Shing{-}Chi Cheung},\n  title        = {Bounded Exhaustive Random Program Generation for Testing Solidity\n                  Compilers and Analyzers},\n  journal      = {CoRR},\n  volume       = {abs/2503.20332},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2503.20332},\n  doi          = {10.48550/ARXIV.2503.20332},\n  eprinttype    = {arXiv},\n  eprint       = {2503.20332},\n  timestamp    = {Sat, 19 Apr 2025 10:31:52 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2503-20332.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "ReuseDroid: A VLM-empowered Android UI Test Migrator Boosted by Active Feedback.",
        "date": "2025-04-03",
        "authors": [
            "Xiaolei Li",
            "Jialun Cao",
            "Yepang Liu",
            "Shing-Chi Cheung",
            "Hailong Wang"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "GUI testing is an essential quality assurance process in mobile app development. However, the creation and maintenance of GUI tests for mobile apps are resource-intensive and costly. Recognizing that many apps share similar functionalities, researchers have proposed various techniques to migrate GUI tests from one app to another with similar features. For example, some techniques employ mapping-based approaches to align the GUI elements traversed by the tests of a source app to those present in the target app. Other test migration techniques have also been proposed to leverage large language models (LLMs) by adapting the GUI tasks in source tests. However, these techniques are ineffective in dealing with different operational logic between the source and target apps. The semantics of GUI elements may not be correctly inferred due to the missing analysis of these flows. In this work, we propose REUSEDROID, a novel multiagent framework for GUI test migration empowered by Large Vision-Language Models (VLMs). REUSEDROID is powered by multiple VLM-based agents, each tackling a stage of the test migration process by leveraging the relevant visual and textual information embedded in GUI pages. An insight of REUSEDROID is to migrate tests based only on the core logic shared across similar apps, while their entire operational logic could differ. We evaluate REUSEDROID on LinPro, a new test migration dataset that consists of 578 migration tasks for 39 popular apps across 4 categories. The experimental result shows that REUSEDROID can successfully migrate 90.3% of the migration tasks, outperforming the best mapping-based and LLM-based baselines by 318.1% and 109.1%, respectively.",
        "arxivUrl": "https://arxiv.org/abs/2504.02357",
        "paperUrl": "https://doi.org/10.48550/arXiv.2504.02357",
        "bibtex": "@article{DBLP:journals/corr/abs-2504-02357,\n  author       = {Xiaolei Li and\n                  Jialun Cao and\n                  Yepang Liu and\n                  Shing{-}Chi Cheung and\n                  Hailong Wang},\n  title        = {ReuseDroid: {A} VLM-empowered Android {UI} Test Migrator Boosted by\n                  Active Feedback},\n  journal      = {CoRR},\n  volume       = {abs/2504.02357},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2504.02357},\n  doi          = {10.48550/ARXIV.2504.02357},\n  eprinttype    = {arXiv},\n  eprint       = {2504.02357},\n  timestamp    = {Tue, 20 May 2025 08:32:19 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2504-02357.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "IP Leakage Attacks Targeting LLM-Based Multi-Agent Systems.",
        "date": "2025-05-18",
        "authors": [
            "Liwen Wang",
            "Wenxuan Wang",
            "Shuai Wang",
            "Zongjie Li",
            "Zhenlan Ji",
            "Zongyi Lyu",
            "Daoyuan Wu",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "The rapid advancement of Large Language Models (LLMs) has led to the emergence of Multi-Agent Systems (MAS) to perform complex tasks through collaboration. However, the intricate nature of MAS, including their architecture and agent interactions, raises significant concerns regarding intellectual property (IP) protection. In this paper, we introduce MASLEAK, a novel attack framework designed to extract sensitive information from MAS applications. MASLEAK targets a practical, black-box setting, where the adversary has no prior knowledge of the MAS architecture or agent configurations. The adversary can only interact with the MAS through its public API, submitting attack query $q$ and observing outputs from the final agent. Inspired by how computer worms propagate and infect vulnerable network hosts, MASLEAK carefully crafts adversarial query $q$ to elicit, propagate, and retain responses from each MAS agent that reveal a full set of proprietary components, including the number of agents, system topology, system prompts, task instructions, and tool usages. We construct the first synthetic dataset of MAS applications with 810 applications and also evaluate MASLEAK against real-world MAS applications, including Coze and CrewAI. MASLEAK achieves high accuracy in extracting MAS IP, with an average attack success rate of 87% for system prompts and task instructions, and 92% for system architecture in most cases. We conclude by discussing the implications of our findings and the potential defenses.",
        "arxivUrl": "https://arxiv.org/abs/2505.12442",
        "paperUrl": "https://doi.org/10.48550/arXiv.2505.12442",
        "bibtex": "@article{DBLP:journals/corr/abs-2505-12442,\n  author       = {Liwen Wang and\n                  Wenxuan Wang and\n                  Shuai Wang and\n                  Zongjie Li and\n                  Zhenlan Ji and\n                  Zongyi Lyu and\n                  Daoyuan Wu and\n                  Shing{-}Chi Cheung},\n  title        = {{IP} Leakage Attacks Targeting LLM-Based Multi-Agent Systems},\n  journal      = {CoRR},\n  volume       = {abs/2505.12442},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2505.12442},\n  doi          = {10.48550/ARXIV.2505.12442},\n  eprinttype    = {arXiv},\n  eprint       = {2505.12442},\n  timestamp    = {Wed, 25 Jun 2025 08:28:59 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2505-12442.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Infi-MMR: Curriculum-based Unlocking Multimodal Reasoning via Phased Reinforcement Learning in Multimodal Small Language Models.",
        "date": "2025-05-29",
        "authors": [
            "Zeyu Liu",
            "Yuhang Liu",
            "Guanghao Zhu",
            "Congkai Xie",
            "Zhen Li",
            "Jianbo Yuan",
            "Xinyao Wang",
            "Qing Li",
            "Shing-Chi Cheung",
            "Shengyu Zhang",
            "Fei Wu",
            "Hongxia Yang"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Recent advancements in large language models (LLMs) have demonstrated substantial progress in reasoning capabilities, such as DeepSeek-R1, which leverages rule-based reinforcement learning to enhance logical reasoning significantly. However, extending these achievements to multimodal large language models (MLLMs) presents critical challenges, which are frequently more pronounced for Multimodal Small Language Models (MSLMs) given their typically weaker foundational reasoning abilities: (1) the scarcity of high-quality multimodal reasoning datasets, (2) the degradation of reasoning capabilities due to the integration of visual processing, and (3) the risk that direct application of reinforcement learning may produce complex yet incorrect reasoning processes. To address these challenges, we design a novel framework Infi-MMR to systematically unlock the reasoning potential of MSLMs through a curriculum of three carefully structured phases and propose our multimodal reasoning model Infi-MMR-3B. The first phase, Foundational Reasoning Activation, leverages high-quality textual reasoning datasets to activate and strengthen the model's logical reasoning capabilities. The second phase, Cross-Modal Reasoning Adaptation, utilizes caption-augmented multimodal data to facilitate the progressive transfer of reasoning skills to multimodal contexts. The third phase, Multimodal Reasoning Enhancement, employs curated, caption-free multimodal data to mitigate linguistic biases and promote robust cross-modal reasoning. Infi-MMR-3B achieves both state-of-the-art multimodal math reasoning ability (43.68% on MathVerse testmini, 27.04% on MathVision test, and 21.33% on OlympiadBench) and general reasoning ability (67.2% on MathVista testmini). Resources are available at this https URL .",
        "arxivUrl": "https://arxiv.org/abs/2505.23091",
        "paperUrl": "https://doi.org/10.48550/arXiv.2505.23091",
        "bibtex": "@article{DBLP:journals/corr/abs-2505-23091,\n  author       = {Zeyu Liu and\n                  Yuhang Liu and\n                  Guanghao Zhu and\n                  Congkai Xie and\n                  Zhen Li and\n                  Jianbo Yuan and\n                  Xinyao Wang and\n                  Qing Li and\n                  Shing{-}Chi Cheung and\n                  Shengyu Zhang and\n                  Fei Wu and\n                  Hongxia Yang},\n  title        = {Infi-MMR: Curriculum-based Unlocking Multimodal Reasoning via Phased\n                  Reinforcement Learning in Multimodal Small Language Models},\n  journal      = {CoRR},\n  volume       = {abs/2505.23091},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2505.23091},\n  doi          = {10.48550/ARXIV.2505.23091},\n  eprinttype    = {arXiv},\n  eprint       = {2505.23091},\n  timestamp    = {Thu, 04 Sep 2025 15:12:12 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2505-23091.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Across Programming Language Silos: A Study on Cross-Lingual Retrieval-augmented Code Generation.",
        "date": "2025-06-04",
        "authors": [
            "Qiming Zhu",
            "Jialun Cao",
            "Xuanang Chen",
            "Yaojie Lu",
            "Hongyu Lin",
            "Xianpei Han",
            "Le Sun",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Current research on large language models (LLMs) with retrieval-augmented code generation (RACG) mainly focuses on single-language settings, leaving cross-lingual effectiveness and security unexplored. Multi-lingual RACG systems are valuable for migrating code-bases across programming languages (PLs), yet face risks from error (e.g. adversarial data corruption) propagation in cross-lingual transfer. We construct a dataset spanning 13 PLs with nearly 14k instances to explore utility and robustness of multi-lingual RACG systems. Our investigation reveals four key insights: (1) Effectiveness: multi-lingual RACG significantly enhances multi-lingual code LLMs generation; (2) Inequality: Java demonstrate superior cross-lingual utility over Python in RACG; (3) Robustness: Adversarial attacks degrade performance significantly in mono-lingual RACG but show mitigated impacts in cross-lingual scenarios; Counterintuitively, perturbed code may improve RACG in cross-lingual scenarios; (4) Specialization: Domain-specific code retrievers outperform significantly general text retrievers. These findings establish foundation for developing effective and secure multi-lingual code assistants.",
        "arxivUrl": "https://arxiv.org/abs/2506.03535",
        "paperUrl": "https://doi.org/10.48550/arXiv.2506.03535",
        "bibtex": "@article{DBLP:journals/corr/abs-2506-03535,\n  author       = {Qiming Zhu and\n                  Jialun Cao and\n                  Xuanang Chen and\n                  Yaojie Lu and\n                  Hongyu Lin and\n                  Xianpei Han and\n                  Le Sun and\n                  Shing{-}Chi Cheung},\n  title        = {Across Programming Language Silos: {A} Study on Cross-Lingual Retrieval-augmented\n                  Code Generation},\n  journal      = {CoRR},\n  volume       = {abs/2506.03535},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2506.03535},\n  doi          = {10.48550/ARXIV.2506.03535},\n  eprinttype    = {arXiv},\n  eprint       = {2506.03535},\n  timestamp    = {Sun, 06 Jul 2025 14:38:46 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2506-03535.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "EmbedAgent: Benchmarking Large Language Models in Embedded System Development.",
        "date": "2025-04-19",
        "authors": [
            "Ruiyang Xu",
            "Jialun Cao",
            "Mingyuan Wu",
            "Wenliang Zhong",
            "Yaojie Lu",
            "Ben He",
            "Xianpei Han",
            "Shing-Chi Cheung",
            "Le Sun"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Large Language Models (LLMs) have shown promise in various tasks, yet few benchmarks assess their capabilities in embedded system development. In this paper, we introduce EmbedAgent, a paradigm designed to simulate real-world roles in embedded system development, such as Embedded System Programmer, Architect, and Integrator. This paradigm enables LLMs to be tested in tasks that bridge the gap between digital and physical systems, allowing for a more comprehensive assessment of their capabilities. To evaluate LLMs on these tasks, we propose Embedbench, the first comprehensive benchmark for embedded system programming, circuit design, and cross-platform migration. Embedbench consists of 126 cases, covering 9 electronic components across 3 hardware platforms. Through extensive experiments on 10 mainstream LLMs, we uncover several key findings. Surprisingly, despite the simplicity of the cases, DeepSeek-R1 achieves only a 55.6% pass@1 rate when provided with schematic information, and 50.0% when tasked with generating the schematics itself. In the cross-platform migration tasks, LLMs show relatively strong performance with MicroPython on the Raspberry Pi Pico (with the top model achieving 73.8% pass@1), but perform poorly on ESP-IDF, where the best model reaches only 29.4% pass@1. Interestingly, we observe that general-purpose chat LLMs like DeepSeek-V3 often fail to utilize relevant pre-trained knowledge in this domain, while reasoning LLMs tend to overthink and overlook efficient knowledge during pretraining. Based on these insights, we propose two strategies: retrieval augmented generation and compiler feedback-to enhance LLM performance. These strategies result in significant improvements, with Deepseek-R1 reaching a 65.1% pass@1 with correct schematics, and 53.1% without. Additionally, the accuracy of the Arduino to ESP32 migration task improves from 21.4% to 27.8%.",
        "arxivUrl": "https://arxiv.org/abs/2506.11003",
        "paperUrl": "https://doi.org/10.48550/arXiv.2506.11003",
        "bibtex": "@article{DBLP:journals/corr/abs-2506-11003,\n  author       = {Ruiyang Xu and\n                  Jialun Cao and\n                  Mingyuan Wu and\n                  Wenliang Zhong and\n                  Yaojie Lu and\n                  Ben He and\n                  Xianpei Han and\n                  Shing{-}Chi Cheung and\n                  Le Sun},\n  title        = {EmbedAgent: Benchmarking Large Language Models in Embedded System\n                  Development},\n  journal      = {CoRR},\n  volume       = {abs/2506.11003},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2506.11003},\n  doi          = {10.48550/ARXIV.2506.11003},\n  eprinttype    = {arXiv},\n  eprint       = {2506.11003},\n  timestamp    = {Sat, 01 Nov 2025 10:14:17 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2506-11003.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "What Builds Effective In-Context Examples for Code Generation?",
        "date": "2025-08-08",
        "authors": [
            "Dongze Li",
            "Songqiang Chen",
            "Jialun Cao",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "In-Context Learning (ICL) has emerged as a promising solution to enhance the code generation capabilities of Large Language Models (LLMs), which incorporates code examples inside the prompt to let LLMs learn from demonstrations. However, despite the substantial effectiveness of the code example-based ICL approach, the specific features (e.g., identifier naming styles, code formatting, solution insight) within the ICL-provided code examples that significantly contribute to the ICL's effectiveness remain unclear. This paper systematically investigates the impact of various code features on ICL with code examples through controlled ablation studies. Our findings reveal that the appropriate naming of variables and functions is crucial for effective code generation, with their elimination leading to performance decreases of up to 30 percentage points. We further demonstrate that LLMs prioritize semantically meaningful identifier names over formatting conventions, with language-specific preferences regarding identifier verbosity. Additionally, our investigation into ICL's potential for enhancing reflection and inference capabilities reveals that current LLMs struggle to extract generalizable problem-solving insights from similar code solutions, despite being capable of utilizing direct information effectively. These findings are expected to provide valuable insights for optimizing ICL systems in code generation applications and highlight fundamental challenges in reflection-based learning for code generation tasks.",
        "arxivUrl": "https://arxiv.org/abs/2508.06414",
        "paperUrl": "https://doi.org/10.48550/arXiv.2508.06414",
        "bibtex": "@article{DBLP:journals/corr/abs-2508-06414,\n  author       = {Dongze Li and\n                  Songqiang Chen and\n                  Jialun Cao and\n                  Shing{-}Chi Cheung},\n  title        = {What Builds Effective In-Context Examples for Code Generation?},\n  journal      = {CoRR},\n  volume       = {abs/2508.06414},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2508.06414},\n  doi          = {10.48550/ARXIV.2508.06414},\n  eprinttype    = {arXiv},\n  eprint       = {2508.06414},\n  timestamp    = {Sat, 13 Sep 2025 14:46:20 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2508-06414.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "RulER: Automated Rule-Based Semantic Error Localization and Repair for Code Translation.",
        "date": "2025-09-18",
        "authors": [
            "Shuo Jin",
            "Songqiang Chen",
            "Xiaoyuan Xie",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Automated code translation aims to convert programs between different programming languages while maintaining their functionality. Due to the imperfections of code translation models, the generated translations may contain errors that compromise their reliability. Existing automated debugging methods for code translation rely on code alignments and repair patch templates to locate and fix erroneous translations. However, existing methods lack reliable references to construct code alignments and design repair patch templates, which significantly impacts their localization accuracy and repair effectiveness. To address these limitations, we reintroduce code translation rules and propose a rule-based debugging method for code translation, called RulER. RulER automatically derives code translation rules from correct translations generated by LLMs, enabling the efficient collection of diverse translation rules. In addition, RulER dynamically combines the existing rules on expandable nodes like expressions and tokens to further adaptively align more statements. These rules capture clear and detailed structural correspondences between source and target programming languages. Therefore, they can serve as reliable and reusable references for code alignment and repair template design, enabling RulER to locate and fix translation errors effectively. Our evaluation of RulER on Java-to-C++ and Python-to-C++ translations produced by four code translation models demonstrates that RulER outperforms state-of-the-art methods, BatFix and TransMap. Our experimental results show that RulER outperformed the best baseline by 20% and 272% in terms of error localization rates and repair success rates, respectively. RulER exhibits superior repair performance compared to directly prompting LLMs for patch generation, demonstrating a promising methodology for extracting and leveraging coding knowledge from LLMs.",
        "arxivUrl": "https://arxiv.org/abs/2509.14829",
        "paperUrl": "https://doi.org/10.48550/arXiv.2509.14829",
        "bibtex": "@article{DBLP:journals/corr/abs-2509-14829,\n  author       = {Shuo Jin and\n                  Songqiang Chen and\n                  Xiaoyuan Xie and\n                  Shing{-}Chi Cheung},\n  title        = {RulER: Automated Rule-Based Semantic Error Localization and Repair\n                  for Code Translation},\n  journal      = {CoRR},\n  volume       = {abs/2509.14829},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2509.14829},\n  doi          = {10.48550/ARXIV.2509.14829},\n  eprinttype    = {arXiv},\n  eprint       = {2509.14829},\n  timestamp    = {Fri, 17 Oct 2025 08:20:35 +0200},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2509-14829.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Can Emulating Semantic Translation Help LLMs with Code Translation? A Study Based on Pseudocode.",
        "date": "2025-10-01",
        "authors": [
            "Songqiang Chen",
            "Congying Xu",
            "Jingyi Chen",
            "Jialun Cao",
            "Jiarong Wu",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Although large language models (LLMs) show promising potential in code translation, they still struggle to generate accurate translations using the commonly adopted direct code-to-code translation approach, which converts an original program into the target programming language (PL) in a single step. Inspired by the success of incorporating intermediate steps to guide LLMs in resolving challenging tasks, in this study, we explore pseudocode-based code translation. This approach emulates human semantic translation by first interpreting the original program's intent and logic into pseudocode and then implementing it in the target PL. To understand the effectiveness of this underexplored approach, we present a systematic empirical study on pseudocode-based code translation, aiming to investigate its helpfulness in enhancing the direct translation approach, illuminate its effective usage, and identify its limitations. By comparing direct and pseudocode-based translation on 9,690 translation tasks across six PLs with five popular LLMs, we found that pseudocode-based translation can effectively complement direct translation, particularly when translating from flexible to rigid PLs and handling a low-training-resource PL. Based on the findings, we suggest combining the translation results of both approaches for test-based selection to leverage their complementary strengths. We also reveal the advantages of pseudocode-based translation in decoupling the code understanding and generation burden on complicated programs and mitigating distractions from PL-specific implementations in original programs, as well as its limitations due to incorrect, incomplete, or ambiguous pseudocode. Our study sheds light on the effective use of pseudocode-based translation and provides evidence to help enhance LLMs in code translation.",
        "arxivUrl": "https://arxiv.org/abs/2510.00920",
        "paperUrl": "https://doi.org/10.48550/arXiv.2510.00920",
        "bibtex": "@article{DBLP:journals/corr/abs-2510-00920,\n  author       = {Songqiang Chen and\n                  Congying Xu and\n                  Jingyi Chen and\n                  Jialun Cao and\n                  Jiarong Wu and\n                  Shing{-}Chi Cheung},\n  title        = {Can Emulating Semantic Translation Help LLMs with Code Translation?\n                  {A} Study Based on Pseudocode},\n  journal      = {CoRR},\n  volume       = {abs/2510.00920},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2510.00920},\n  doi          = {10.48550/ARXIV.2510.00920},\n  eprinttype    = {arXiv},\n  eprint       = {2510.00920},\n  timestamp    = {Sat, 08 Nov 2025 10:18:14 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2510-00920.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Testing and Enhancing Multi-Agent Systems for Robust Code Generation.",
        "date": "2025-10-12",
        "authors": [
            "Zongyi Lyu",
            "Songqiang Chen",
            "Zhenlan Ji",
            "Liwen Wang",
            "Shuai Wang",
            "Daoyuan Wu",
            "Wenxuan Wang",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Multi-agent systems (MASs) have emerged as a promising paradigm for automated code generation, demonstrating impressive performance on established benchmarks. Despite their prosperous development, the fundamental mechanisms underlying their robustness remain poorly understood, raising critical concerns for real-world deployment. This paper conducts a systematic empirical study to uncover the internal robustness flaws of MASs using a mutation-based methodology. By designing a testing pipeline incorporating semantic-preserving mutation operators and a novel fitness function, we assess mainstream MASs across multiple datasets and LLMs. Our findings reveal substantial robustness flaws: semantically equivalent inputs cause drastic performance drops, with MASs failing to solve 7.9\\%--83.3\\% of problems they initially resolved successfully. Through comprehensive failure analysis, we discover a fundamental cause underlying these robustness issues: the \\textit{planner-coder gap}, which accounts for 75.3\\% of failures. This gap arises from information loss in the multi-stage transformation process where planning agents decompose requirements into underspecified plans, and coding agents subsequently misinterpret intricate logic during code generation. Based on this formulated information transformation process, we propose a \\textit{repairing method} that mitigates information loss through multi-prompt generation and introduces a monitor agent to bridge the planner-coder gap. Evaluation shows that our repairing method effectively enhances the robustness of MASs by solving 40.0\\%--88.9\\% of identified failures. Our work uncovers critical robustness flaws in MASs and provides effective mitigation strategies, contributing essential insights for developing more reliable MASs for code generation.",
        "arxivUrl": "https://arxiv.org/abs/2510.10460",
        "paperUrl": "https://doi.org/10.48550/arXiv.2510.10460",
        "bibtex": "@article{DBLP:journals/corr/abs-2510-10460,\n  author       = {Zongyi Lyu and\n                  Songqiang Chen and\n                  Zhenlan Ji and\n                  Liwen Wang and\n                  Shuai Wang and\n                  Daoyuan Wu and\n                  Wenxuan Wang and\n                  Shing{-}Chi Cheung},\n  title        = {Testing and Enhancing Multi-Agent Systems for Robust Code Generation},\n  journal      = {CoRR},\n  volume       = {abs/2510.10460},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2510.10460},\n  doi          = {10.48550/ARXIV.2510.10460},\n  eprinttype    = {arXiv},\n  eprint       = {2510.10460},\n  timestamp    = {Tue, 11 Nov 2025 13:12:33 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2510-10460.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Optimization-Aware Test Generation for Deep Learning Compilers.",
        "date": "2025-11-24",
        "authors": [
            "Qingchao Shen",
            "Zan Wang",
            "Haoyang Ma",
            "Yongqiang Tian",
            "Lili Huang",
            "Zibo Xiao",
            "Junjie Chen",
            "Shing-Chi Cheung"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Deep Learning (DL) compilers have been widely utilized to optimize DL models for efficient deployment across various hardware. Due to their vital role in the DL ecosystem, ensuring their reliability and security is critical. However, existing approaches have limitations in testing optimization stages, which is the core functionality of DL compilers, due to the difficulty in generating optimization-aware tests. In this paper, we proposed OATest, a novel approach for synthesizing optimization-aware computational graphs. The approach combines patterns extracted from documented tests for optimization and incorporates them into seed computational graphs, enabling broader exploration of optimization paths. To guarantee the optimization-awareness of generated graphs, OATest introduces the edges reusing strategy to establish strong connections between patterns and contexts. Additionally, to solve the validity challenge for the generated graphs, OATest employs an auxiliary layers addition strategy to resolve broken constraints. Equipped with two distinct test oracles, OATest applies differential testing to evaluate the two widely used DL compilers (i.e., TVM and ONNXRuntime). Our experimental results show that OATest outperforms the state-of-the-art method by detecting more bugs and achieving higher code coverage in TVM and ONNXRutimes. Additionally, OATest uncovers 58 previously unknown bugs, 36 of which have been confirmed or fixed by developers.",
        "arxivUrl": "https://arxiv.org/abs/2511.18918",
        "paperUrl": "https://doi.org/10.48550/arXiv.2511.18918",
        "bibtex": "@article{DBLP:journals/corr/abs-2511-18918,\n  author       = {Qingchao Shen and\n                  Zan Wang and\n                  Haoyang Ma and\n                  Yongqiang Tian and\n                  Lili Huang and\n                  Zibo Xiao and\n                  Junjie Chen and\n                  Shing{-}Chi Cheung},\n  title        = {Optimization-Aware Test Generation for Deep Learning Compilers},\n  journal      = {CoRR},\n  volume       = {abs/2511.18918},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2511.18918},\n  doi          = {10.48550/ARXIV.2511.18918},\n  eprinttype    = {arXiv},\n  eprint       = {2511.18918},\n  timestamp    = {Wed, 14 Jan 2026 20:46:47 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2511-18918.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    },
    {
        "title": "Multi-Agent Systems for Dataset Adaptation in Software Engineering: Capabilities, Limitations, and Future Directions.",
        "date": "2025-11-26",
        "authors": [
            "Jingyi Chen",
            "Xiaoyan Guo",
            "Songqiang Chen",
            "Shing-Chi Cheung",
            "Jiasi Shen"
        ],
        "venue": "",
        "venueShort": "",
        "abstract": "Automating the adaptation of software engineering (SE) research artifacts across datasets is essential for scalability and reproducibility, yet it remains largely unstudied. Recent advances in large language model (LLM)-based multi-agent systems, such as GitHub Copilot's agent mode, promise to automate complex development workflows through coordinated reasoning, code generation, and tool interaction. This paper presents the first empirical study on how state-of-the-art multi-agent systems perform in dataset adaptation tasks. We evaluate Copilot, backed by GPT-4.1 and Claude Sonnet 4, on adapting SE research artifacts from benchmark repositories including ROCODE and LogHub2.0. Through a five-stage evaluation pipeline (file comprehension, code editing, command generation, validation, and final execution), we measure success rates, analyze failure patterns, and assess prompt-based interventions designed to enhance agent performance. Results show that current systems can identify key files and generate partial adaptations but rarely produce functionally correct implementations. Prompt-level interventions, especially providing execution error messages and reference code, substantially improve structural similarity to ground truth (from 7.25% to 67.14%), highlighting the importance of contextual and feedback-driven guidance. Our findings reveal both the promise and limitations of today's multi-agent LLM systems for dataset adaptation, and suggest concrete directions for building more reliable, self-correcting agents in future SE research.",
        "arxivUrl": "https://arxiv.org/abs/2511.21380",
        "paperUrl": "https://doi.org/10.48550/arXiv.2511.21380",
        "bibtex": "@article{DBLP:journals/corr/abs-2511-21380,\n  author       = {Jingyi Chen and\n                  Xiaoyan Guo and\n                  Songqiang Chen and\n                  Shing{-}Chi Cheung and\n                  Jiasi Shen},\n  title        = {Multi-Agent Systems for Dataset Adaptation in Software Engineering:\n                  Capabilities, Limitations, and Future Directions},\n  journal      = {CoRR},\n  volume       = {abs/2511.21380},\n  year         = {2025},\n  url          = {https://doi.org/10.48550/arXiv.2511.21380},\n  doi          = {10.48550/ARXIV.2511.21380},\n  eprinttype    = {arXiv},\n  eprint       = {2511.21380},\n  timestamp    = {Wed, 14 Jan 2026 21:10:58 +0100},\n  biburl       = {https://dblp.org/rec/journals/corr/abs-2511-21380.bib},\n  bibsource    = {dblp computer science bibliography, https://dblp.org}\n}"
    }
]