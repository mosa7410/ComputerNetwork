import matplotlib.pyplot as plt
import concurrent.futures
import ras_client

client_10_list = []
client_20_list = []
client_30_list = []

def multiprocess_func() :
    with concurrent.futures.ProcessPoolExecutor(max_workers = 10) as executor:
        for i in range(0, 10) :
            f = executor.submit(ras_client.getDownloadTime)
            client_10_list.append(f.result())

    with concurrent.futures.ProcessPoolExecutor(max_workers = 20) as executor:
        for i in range(0, 20) :
            f = executor.submit(ras_client.getDownloadTime)
            client_20_list.append(f.result())

    with concurrent.futures.ProcessPoolExecutor(max_workers = 30) as executor:
        for i in range(0, 30) :
            f = executor.submit(ras_client.getDownloadTime)
            client_30_list.append(f.result())

def vs() :
    box_plot_data = [client_10_list, client_20_list, client_30_list]
    plt.boxplot(box_plot_data)
    plt.xlabel("Number of Clients")
    plt.ylabel("Download Time(s)")
    plt.xticks([1,2,3],[10,20,30])
    plt.show()

if __name__ == "__main__" :
    multiprocess_func()
    vs()
