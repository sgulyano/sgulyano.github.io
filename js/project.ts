// 1. Select the div element using the id property
const app = document.getElementById("project-div");

class Project {
    //field 
    title: string;
    text: string;
    img: string;
    url: string;

    //constructor 
    constructor(title: string, text: string, img: string, url: string) {
        this.title = title
        this.text = text
        this.img = img
        this.url = url
    }

    //function 
    disp() {
        const elem = document.createElement("div");
        elem.classList.add("col-auto", "mb-3");

        const card = document.createElement("div");
        card.classList.add("card", "proj-card");
        card.setAttribute("style", "width: 21rem;");
        elem?.appendChild(card);

        const view = document.createElement("div");
        view.classList.add("view", "overlay");
        card?.appendChild(view);

        const img = document.createElement("img");
        img.classList.add("card-img-top");
        img.setAttribute("src", this.img);
        view?.appendChild(img);

        const card_body = document.createElement("div");
        card_body.classList.add("card-body");
        card?.appendChild(card_body);

        const title = document.createElement("h4");
        title.classList.add("card-title");
        title.textContent = this.title
        card_body?.appendChild(title);

        const text = document.createElement("p");
        text.classList.add("card-text");
        text.textContent = this.text
        card_body?.appendChild(text);

        const button = document.createElement("a");
        button.classList.add("btn", "btn-primary", "stretched-link");
        button.setAttribute("href", this.url);
        button.setAttribute("target", "_blank");
        button.textContent = "Read More"
        card_body?.appendChild(button);

        return elem
    }
}

let myproj: Project[] = [
    new Project("Data Visualization of Crime and Justice System Data and Statistics",
        `In collaboration with the Office of Justice Affairs, this project aims to enhance the integration of justice system data, improve the effectiveness of criminal justice policies, and provide insights for crime prevention and international reporting.`,
        "img/proj/oja.png",
        "https://www.oja.go.th/justicedata/"),
    new Project("Semanthai Bank: Thai Corpus and Benchmarks on Automated Semantic Role Annotation",
        "This project introduces a new system to streamline the creation of lexical resources, particularly for Thai VerbNet, and presents the first prototype of a Thai VerbNet corpus. It also includes an overview of semantic role labeling algorithms and a new verb classification method, offering a baseline for future research.",
        "img/proj/semanthai.png",
        "https://sgulyano.github.io/semanthaibank/"),
    new Project("Deep Learning for Raman Spectral Analysis",
        "In collaboration with the Center of Excellence in Functional Advanced Materials Engineering Research Center (CoE FAME) and Western Digital (WD), this project proposes using deep learning techniques for the automatic analysis of Raman spectra to enhance contamination detection in HDDs.",
        "img/proj/raman.jpg",
        "https://ieeexplore.ieee.org/document/10637964"),
    new Project("Efficient Microplastic Detection Using Computational and Spectroscopic Methods",
        "This project develops a machine learning technique for analyzing FT-IR spectra of microplastics, improving detection accuracy and creating a dataset for various types. This aims to advance machine learning and enhance environmental management strategies against microplastic pollution.",
        "img/proj/ftir.png",
        "https://doi.org/10.1038/s41598-024-70407-5"),
];

// let a = myskill[0].disp()

for (let proj of myproj) {
    let elem = proj.disp();
    app?.appendChild(elem);
} 