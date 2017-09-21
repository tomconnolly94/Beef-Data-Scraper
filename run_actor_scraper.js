var PythonShell = require('python-shell');

var options = {};

//config options based on current OS
if(/^win/.test(process.platform)){ //Windows

    options = {
        mode: 'text',
        //pythonPath: 'C:\Users\Tom.DESKTOP-D3OBC42\AppData\Local\Programs\Python\Python36-32\python',
        pythonPath: 'C:/Users/Tom.DESKTOP-D3OBC42/AppData/Local/Programs/Python/Python36-32/python',
        pythonOptions: ['-u'],
        scriptPath: 'C:/Users/Tom.DESKTOP-D3OBC42/beeftracker/news_scraping_project/beeftracker_scraping',
        args: ['Dwayne Johnson']
    };
}
else{ //Linux
     options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: '/home/tom/beeftracker/news_scraping_project/beeftracker_scraping',
        args: ['Dwayne Johnson']
    };
}

PythonShell.run('scrape_actor.py', options, function (err, results) {
	if (err) throw err;
	// results is an array consisting of messages collected during execution
	console.log('results: %j', results);
});
