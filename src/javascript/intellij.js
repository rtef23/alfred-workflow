const path = require("path");
const fs = require("fs");

const INTELLIJ_META_DIRECTORY = '.idea';
const INTELLIJ_META_NAME_FILE = '.idea/.name';

const PATH_SEPARATOR = '/';

const ENCODING = 'UTF-8'
const PROJECT_ROOT_DIRECTORIES = [
    '/Users/songjooyoung/private-projects',
];

const query = process.argv[2];

console.log(JSON.stringify({
    items: enumerateProjectDirectories()
        .filter(({ projectName }) => {
            if(query){
                return projectName.includes(query);
            }else{
                return true;
            }
        })
        .map(({ projectName, projectDirectory }) => ({
            uid: projectName,
            title: projectName,
            arg: projectDirectory
        }))
}));

function enumerateProjectDirectories() {
    return PROJECT_ROOT_DIRECTORIES
        .flatMap(rootDirectory => {
            const files = fs.readdirSync(rootDirectory, {encoding: ENCODING, withFileTypes: true});

            return files
                .filter(file => file.isDirectory)
                .map(({ name }) => ({
                    projectDirectory: path.join(rootDirectory, name)
                }))
                .filter(({ projectDirectory }) => isIntelliJProject(projectDirectory))
                .map(({ projectDirectory, ...rest }) => ({
                    projectDirectory,
                    projectName: getProjectName(projectDirectory),

                    ...rest
                }));
        });
}

function isIntelliJProject(projectPath) {
    return fs.existsSync(path.join(projectPath, INTELLIJ_META_DIRECTORY));
}

function getProjectName(projectPath) {
    const meta_name_file = path.join(projectPath, INTELLIJ_META_NAME_FILE);

    if(fs.existsSync(meta_name_file)){
        return fs.readFileSync(meta_name_file, {
            encoding: ENCODING,
            flag: 'r'
        });
    }else{
        return projectPath.split(PATH_SEPARATOR).at(-1);
    }
}