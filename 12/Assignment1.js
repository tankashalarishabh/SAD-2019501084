var z = "Build"
var z1 = "build"
var z2 = "Build"
var student1 = {
    height : 150 ,
    weight : 70
}
var student2 = {
    height : 150 ,
    weight : 70 ,
    age : 21
}

var student3 = {
    height : 150 ,
    weight : 70
}

var a1 = deepEqual(z , z1)
console.log(a1)
var a2 = deepEqual(z , z2)
console.log(a2)
var a3 = deepEqual(student1 , student2)
console.log(a3)
var a4 = deepEqual(student1, student3)
console.log(a4)



var a = 'e'
var x = countBs(z)
var y = countChar(z,a)


function countBs(z) {
    var n = 0
    for (var i = 0;i < z.length; i++) {
        if (z.charAt(i) === "B") {
            n = n + 1
        }
    }console.log(n)
}

function countChar(z,a) {
    var n = 0
    for (var i = 0;i < z.length;i++) {
        if (z.charAt(i) == a) {
            n = n + 1
        }
    }console.log(n)
}

function deepEqual(a,b) {
    if (typeof a === typeof b) {
        // console.log("entered")
        var aobj = Object.getOwnPropertyNames(a);
        var bobj = Object.getOwnPropertyNames(b);
        // console.log(aobj)
        if (aobj.length != bobj.length) {
            return false
        }

        for (var i = 0; i < aobj.length; i++) {
            var name = aobj[i];
            // console.log("this is name ",name)

            if (a[name] !== b[name]) {
                // console.log("this is",a[name])
                return false
            }
        }

        return true
    }

}