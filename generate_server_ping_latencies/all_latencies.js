// Taken from https://github.com/mda590/cloudping.co/issues/35.
const got = require('got');
const cheerio = require('cheerio');

(async function() {
    const result = {};

    const html = (await got('https://www.cloudping.co/grid/p_50/timeframe/1Y')).body;
    const $ = cheerio.load(html);
    const destRegions = $('#app > table > thead > tr > th')
        .slice(1)
        .map((i, el) => {
            const splt = $(el).text().split(' ');
            return splt.pop();
        })
        .toArray();

    $('#app > table > tbody > tr')
        .map((i, el) => {
            const splt = $(el).find('th').first().text().split(' ');
            const src = splt.pop();
            $(el)
                .find('td')
                .map((i, el) => $(el).text())
                .toArray()
                .map((v, i) => {
                    if(!result[src]) {
                        result[src] = {};
                    }
                    result[src][destRegions[i]] = +v;
                });
        });
    console.log(JSON.stringify(result, null, 2));
})()