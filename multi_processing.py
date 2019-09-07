from multiprocessing import Pool,cpu_count
from scrapper import historical_data

class multiProcessing(object):
    def __init__(self):
        self.MAXIMUM_PROCESSING = int(cpu_count()/4)
        self.workers = Pool(self.MAXIMUM_PROCESSING)
        self.historical_data = historical_data()

    def jobs(self):
        Country_IDs = self.historical_data.search()["country_IDs"]
        self.workers.map(self.historical_data.get_company_stocks, Country_IDs)
        self.workers.terminate()
        self.workers.join()

if __name__ == "__main__":
    print(cpu_count())
    mp = multiProcessing()
    mp.jobs()