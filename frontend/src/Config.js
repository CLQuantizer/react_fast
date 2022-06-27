class Config {
  constructor() {
    this.developmentServer = 'http://localhost:3000/';
    this.productionServer = 'http://langedev.net/';
    this.developmentApi = 'http://localhost:8000/';
    this.productionApi = 'http://langedev.net:8000/';
  }
}

export default new Config();