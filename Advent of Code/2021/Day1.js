let readInputFile = require('./readInputFile.js')

let inputData = readInputFile.getInput(1).split('\n').map((v) => {
    return parseInt(v.replace('\r', ''));
});

let last = Infinity;
let increaseCount = 0;

for (let i of inputData) {
    if (i > last) {
        increaseCount++
    }
    last = i;
}

console.log('Part 1:', increaseCount);

last = Infinity;
increaseCount = 0;
let slidingSums = [0, 0, 0]

inputData.forEach((val, index) => {
    if (index >= 3) {
        if (slidingSums[index % 3] > last) {
            increaseCount++;
        }
        last = slidingSums[index % 3]
    }
    slidingSums[index % 3] = 0;
    for (let x = index; x < index + 3; x++) {
        slidingSums[x % 3] += val;
    }
})

console.log('Part 2:', increaseCount);
