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
        button.textContent = "Open"
        card_body?.appendChild(button);

        return elem
        // var parser = new DOMParser();
        // var doc = parser.parseFromString(`
        // <div class="col-auto mb-3 d-print-inline-flex">
        //     <div class="card" style="width: 18rem;">
        //         <div class="view overlay">
        //             <img class="card-img-top"
        //                 src="${this.img}"
        //                 alt="Card image cap">
        //             <a href="#!">
        //                 <div class="mask rgba-white-slight"></div>
        //             </a>
        //         </div>

        //         <div class="card-body">
        //             <h4 class="card-title">${this.title}</h4>
        //             <p class="card-text">
        //             ${this.text}
        //             </p>
        //             <a href="${this.url}" class="btn btn-primary stretched-link">Open</a>
        //         </div>        
        //     </div>
        // </div>`, 'text/html');

        // return doc.body;
    }

    // //function 
    // disp() {
    //     var parser = new DOMParser();
    //     var doc = parser.parseFromString(`
    //     <div class="col-auto mb-3">
    //         <div class="card" style="width: 15rem;">
    //             <div class="card-body">
    //                 <h5 class="card-title">Card title</h5>
    //                 <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
    //                 <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    //                 <a href="#" class="card-link">Card link</a>
    //                 <a href="#" class="card-link">Another link</a>
    //             </div>
    //         </div>
    //     </div>`, 'text/html');

    //     return doc.body;
    // }
}

let myproj: Project[] = [
    new Project("Image Classification บน Jetson Nano",
        `เล่าวิธีการทำ Image Classification โดยใช้เทคนิค Deep Learning รันบน NVIDIA Jetson Nano 
        ผ่าน Library ที่มีชื่อว่า TensorFlow และ TensorRT`,
        "img/proj/jetson.png",
        "https://medium.com/@sgulyano/introduction-to-deep-learning-on-nvidia-jetson-nano-87428b3c6e17"),
    new Project("หลักสูตร AI Level 3",
        "จัดทำโดย สสวท.",
        "img/proj/ipst.png",
        "https://www.ipst.ac.th/news/13757/20210727_ai-level3.html"),
    new Project("Project: Semanthai Bank",
        "Lexical resources have played a key role in advancing natural language processing research. One particular resource is VerbNet, which contains both syntactic and semantic information of verbs. Read more ...",
        "img/proj/semanthai.png",
        "https://github.com/sgulyano/semanthaibank"),
];

// let a = myskill[0].disp()

for (let proj of myproj) {
    let elem = proj.disp();
    app?.appendChild(elem);
} 