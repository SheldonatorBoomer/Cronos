/project-root
├── /server                         # Node.js Web Server
│   ├── app.js                      # Entry point for the web server
│   ├── /controllers                # API route controllers
│   │   └── searchController.js     # Logic for handling requests to Search.py
│   ├── /routes                     # API routes for the server
│   │   └── searchRoutes.js         # Routes for Search.py
│   ├── /services                   # Services for integrating with Python scripts
│   │   └── searchService.js        # Service that invokes Search.py
│   └── /config                     # Configuration files
│       └── config.js               # Configuration file for the server, paths, etc.
├── /python-scripts                 # Python scripts
│   ├── /database                   # Database initialization and management
│   │   └── initialise.py           # Database setup file
│   ├── /crawler                    # Web crawling scripts
│   │   ├── URLCrawler.py           # Crawler script
│   │   └── scrapUrl.py             # Helper file for URLCrawler.py
│   ├── /search                     # Search functionality
│   │   └── Search.py               # Search script
│   └── requirements.txt            # List of Python dependencies
└── /node_modules                   # Node.js modules
└── package.json                    # Node.js project metadata
└── README.md                       # Project overview and documentation
