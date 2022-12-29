// 1. Select the div element using the id property
var app = document.getElementById("project-div");
var Project = /** @class */ (function () {
    //constructor 
    function Project(title, text, img, url) {
        this.title = title;
        this.text = text;
        this.img = img;
        this.url = url;
    }
    //function 
    Project.prototype.disp = function () {
        var elem = document.createElement("div");
        elem.classList.add("col-auto", "mb-3");
        var card = document.createElement("div");
        card.classList.add("card", "proj-card");
        card.setAttribute("style", "width: 21rem;");
        elem === null || elem === void 0 ? void 0 : elem.appendChild(card);
        var view = document.createElement("div");
        view.classList.add("view", "overlay");
        card === null || card === void 0 ? void 0 : card.appendChild(view);
        var img = document.createElement("img");
        img.classList.add("card-img-top");
        img.setAttribute("src", this.img);
        view === null || view === void 0 ? void 0 : view.appendChild(img);
        var card_body = document.createElement("div");
        card_body.classList.add("card-body");
        card === null || card === void 0 ? void 0 : card.appendChild(card_body);
        var title = document.createElement("h4");
        title.classList.add("card-title");
        title.textContent = this.title;
        card_body === null || card_body === void 0 ? void 0 : card_body.appendChild(title);
        var text = document.createElement("p");
        text.classList.add("card-text");
        text.textContent = this.text;
        card_body === null || card_body === void 0 ? void 0 : card_body.appendChild(text);
        var button = document.createElement("a");
        button.classList.add("btn", "btn-primary", "stretched-link");
        button.setAttribute("href", this.url);
        button.textContent = "Open";
        card_body === null || card_body === void 0 ? void 0 : card_body.appendChild(button);
        return elem;
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
    };
    return Project;
}());
var myproj = [
    new Project("Image Classification บน Jetson Nano", "\u0E40\u0E25\u0E48\u0E32\u0E27\u0E34\u0E18\u0E35\u0E01\u0E32\u0E23\u0E17\u0E33 Image Classification \u0E42\u0E14\u0E22\u0E43\u0E0A\u0E49\u0E40\u0E17\u0E04\u0E19\u0E34\u0E04 Deep Learning \u0E23\u0E31\u0E19\u0E1A\u0E19 NVIDIA Jetson Nano \n        \u0E1C\u0E48\u0E32\u0E19 Library \u0E17\u0E35\u0E48\u0E21\u0E35\u0E0A\u0E37\u0E48\u0E2D\u0E27\u0E48\u0E32 TensorFlow \u0E41\u0E25\u0E30 TensorRT", "img/proj/jetson.png", "https://medium.com/@sgulyano/introduction-to-deep-learning-on-nvidia-jetson-nano-87428b3c6e17"),
    new Project("หลักสูตร AI Level 3", "จัดทำโดย สสวท.", "img/proj/ipst.png", "https://teacherpd.ipst.ac.th/"),
];
// let a = myskill[0].disp()
for (var _i = 0, myproj_1 = myproj; _i < myproj_1.length; _i++) {
    var proj = myproj_1[_i];
    var elem = proj.disp();
    app === null || app === void 0 ? void 0 : app.appendChild(elem);
}
