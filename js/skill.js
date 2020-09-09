// 1. Select the div element using the id property
var leftcol = document.getElementById("left-skill-div");
var rightcol = document.getElementById("right-skill-div");
// const app = document.getElementById("skill-div");
// const leftcol = document.createElement("div");
// leftcol.classList.add("col-sm-6", "col-xs-12");
// // leftcol.appendChild(a)
// const rightcol = document.createElement("div");
// rightcol.classList.add("col-sm-6", "col-xs-12");
// app?.appendChild(leftcol);
// app?.appendChild(rightcol);
var Skill = /** @class */ (function () {
    //constructor 
    function Skill(name, level, color) {
        this.name = name;
        this.level = level;
        this.color = color;
    }
    //function 
    Skill.prototype.disp = function () {
        var elem = document.createElement("div");
        var title = document.createElement("h3");
        title.classList.add("progress-title");
        title.textContent = this.name;
        var progress = document.createElement("div");
        progress.classList.add("progress");
        var progress_bar = document.createElement("div");
        progress_bar.classList.add("progress-bar");
        if (this.color) {
            progress_bar.classList.add(this.color);
        }
        progress_bar.setAttribute("style", "width: " + this.level + "%;");
        progress === null || progress === void 0 ? void 0 : progress.appendChild(progress_bar);
        var progress_value = document.createElement("div");
        progress_value.classList.add("progress-value");
        progress_value.textContent = this.level + "%";
        progress_bar === null || progress_bar === void 0 ? void 0 : progress_bar.appendChild(progress_value);
        elem === null || elem === void 0 ? void 0 : elem.appendChild(title);
        elem === null || elem === void 0 ? void 0 : elem.appendChild(progress);
        return elem;
        // var parser = new DOMParser();
        // var doc = parser.parseFromString(`<h3 class="progress-title">${this.name}</h3>
        // <div class="progress">
        //     <div class="progress-bar ${this.color}" style="width: ${this.level}%;">
        //         <div class="progress-value">${this.level}%</div>
        //     </div>
        // </div>`, 'text/html');
        // return doc.body;
    };
    return Skill;
}());
var myskill = [
    new Skill("Python", 100, ""),
    new Skill("Matlab", 100, ""),
    new Skill("C/C++", 70, ""),
    new Skill("Java/Android", 50, ""),
    new Skill("R", 50, ""),
    new Skill("Tensorflow/Keras", 50, "bg-danger"),
    new Skill("PyTorch", 30, "bg-danger"),
    new Skill("Caffe", 30, "bg-danger"),
    new Skill("VTK", 60, "bg-warning"),
    new Skill("OpenCV", 70, "bg-warning"),
    new Skill("HTML/CSS/Bootstrap", 40, "bg-info"),
    new Skill("Django", 40, "bg-info"),
    new Skill("Flask", 40, "bg-info"),
    new Skill("SQL", 70, "bg-success"),
    new Skill("MongoDB", 30, "bg-success"),
    new Skill("Git", 60, "bg-success"),
    new Skill("Docker", 50, "bg-success"),
];
// let a = myskill[0].disp()
for (var i = 0; i < myskill.length; i++) {
    var elem = myskill[i].disp();
    if (i % 2 == 0) {
        leftcol.append(elem);
    }
    else {
        rightcol.append(elem);
    }
}
