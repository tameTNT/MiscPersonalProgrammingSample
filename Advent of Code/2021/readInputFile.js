const fs = require('fs');

exports.getInput = (day) => {
    return fs.readFileSync(`./Inputs/Day${day}.txt`).toString();
}
