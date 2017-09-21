var PythonShell = require('python-shell');

var options = {
	mode: 'text',
	pythonPath: '/usr/bin/python3',
	pythonOptions: ['-u'],
	scriptPath: '/home/tom/beeftracker/news_scraping_project/beeftracker_scraping',
	args: ['Dwayne Johnson']
};

PythonShell.run('scrape_actor.py', options, function (err, results) {
	if (err) throw err;
	// results is an array consisting of messages collected during execution
	console.log('results: %j', results);
});
