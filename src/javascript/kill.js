import psList from 'ps-list';
import os from 'os';
import _ from 'lodash';
import { execSync, exec } from 'child_process';

const query = process.argv[2];

psList()
    .then((psListProcesses) => {
        const portSearchResult = execSync(`lsof -P | grep :${query} | awk '{print $2, $8 $9}'`, { stdio: 'pipe' })
            .toString()
            .split("\n")
            .filter((line) => !!line)
            .map((line) => {
                const processInfo = line.split(" ");

                return ({
                    pid: processInfo[0],
                    portInfo: processInfo[1]
                });
            });

        const items = _.union(
            portSearchResult
                .map(({ pid, portInfo }) => {
                    return ({
                       title: `(${pid}) ${portInfo}`,
                       subtitle: `Port Search result`,
                       arg: pid
                   });
                }),

            psListProcesses
                .filter(({ name }) => {
                    if(query){
                        return name.includes(query);
                    }else{
                        return true;
                    }
                })
                .map(({pid, name, cmd}) => ({
                    title: `(${pid}) ${name} [${cmd}]`,
                    subtitle: `Name Search result`,
                    arg: pid
                }))
        );

        console.log(JSON.stringify({ items }));
    })
    .catch((error) => console.log);