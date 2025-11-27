// Sample JavaScript Code for Testing

var globalVar = "This should be const or let";

function calculateSum(arr) {
    var sum = 0;
    for (var i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
    
    getInfo() {
        return `${this.name} (${this.email})`;
    }
    
    isValidEmail() {
        return this.email.includes('@');
    }
}

function main() {
    const numbers = [1, 2, 3, 4, 5];
    console.log("Sum:", calculateSum(numbers));
    
    const user = new User("John Doe", "john@example.com");
    console.log("User:", user.getInfo());
    console.log("Valid email:", user.isValidEmail());
}

main();