
export default {
    pathToString: function(path) {

        // Ensure we have at least one item
        if (path.length === 0) {
            throw "Invalid path"
        }

        // Ensure the first element is a root element
        if (path[0] !== "") {
            throw "Invalid path"
        }

        if (path.length === 1) {
            // return the string for a root path
            return "/"
        } else {
            // return the string for a non root path
            // encode any URI components taht may have consiquenses
            let escapedPath = []
            for (let part of path) {
                part = encodeURIComponent(part)
                escapedPath.push(part)
            }
            return escapedPath.join("/")
        }
    },
}
