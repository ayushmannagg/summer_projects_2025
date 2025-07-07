let a = Math.floor(Math.random() * 100) + 1;
let attempts = 0;
// console.log(a);
let running = true;
while (running) {
    const x = prompt("Enter your Guessed number:");
    attempts++;
    if (x > a) {
        console.log("Your guess is greater than the original number")
    } else if (x < a) {
        console.log("Your guess is lower than the original number")
    }
    // chances++; console.log(chances)
    else {
        console.log("You have guessed the correct number")
        console.log("your score is : ", attempts)
        break
    }
}