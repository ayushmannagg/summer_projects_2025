console.log(window)
console.log(document)
document.body.style.background = "yellow"


let runAgain = true;
const canDrive = (age) => {
    return age >= 18 ? true : false
}
while (runAgain) {
    let age = prompt("Enter YOUR AGE")
    age = Number.parseInt(age)
    if (age < 0) {
        console.error("Pease enter a valid age")
        break
    }
    if (canDrive(age)) {
        alert("yes you can drive")
    } else {
        alert("you cannot drive")
    }
    runAgain = confirm("do you want to check again?")
}