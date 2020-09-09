// 1. Select the div element using the id property
const leftcol = document.getElementById("left-skill-div");
const rightcol = document.getElementById("right-skill-div");

// const app = document.getElementById("skill-div");

// const leftcol = document.createElement("div");
// leftcol.classList.add("col-sm-6", "col-xs-12");

// // leftcol.appendChild(a)
// const rightcol = document.createElement("div");
// rightcol.classList.add("col-sm-6", "col-xs-12");

// app?.appendChild(leftcol);
// app?.appendChild(rightcol);


class Skill {
    //field 
    name: string;
    level: number;
    color: string;

    //constructor 
    constructor(name: string, level: number, color: string) {
        this.name = name
        this.level = level
        this.color = color
    }

    //function 
    disp() {

        const elem = document.createElement("div");

        const title = document.createElement("h3");
        title.classList.add("progress-title");
        title.textContent = this.name

        const progress = document.createElement("div");
        progress.classList.add("progress");
        const progress_bar = document.createElement("div");
        progress_bar.classList.add("progress-bar");
        if (this.color) {
            progress_bar.classList.add(this.color);
        }
        progress_bar.setAttribute("style", "width: "+this.level+"%;");
        progress?.appendChild(progress_bar);

        const progress_value = document.createElement("div");
        progress_value.classList.add("progress-value");
        progress_value.textContent = this.level + "%"
        progress_bar?.appendChild(progress_value);

        elem?.appendChild(title);
        elem?.appendChild(progress);
        return elem;


        // var parser = new DOMParser();
        // var doc = parser.parseFromString(`<h3 class="progress-title">${this.name}</h3>
        // <div class="progress">
        //     <div class="progress-bar ${this.color}" style="width: ${this.level}%;">
        //         <div class="progress-value">${this.level}%</div>
        //     </div>
        // </div>`, 'text/html');
        // return doc.body;
    }
}

let myskill: Skill[] = [
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
    let elem = myskill[i].disp()
    if (i % 2 == 0) {
        leftcol.append(elem);
    } else {
        rightcol.append(elem);
    }
}
