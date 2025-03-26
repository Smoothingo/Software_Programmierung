#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

int hello_interval = 1;
int servus_interval = 1;
std::mutex interval_mutex;

void printHello() {
    auto last_time = std::chrono::steady_clock::now();
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        auto now = std::chrono::steady_clock::now();
        std::lock_guard<std::mutex> lock(interval_mutex);
        if (std::chrono::duration_cast<std::chrono::seconds>(now - last_time).count() >= hello_interval) {
            std::cout << "Hallo" << std::endl;
            last_time = now;
        }
    }
}

void printServus() {
    auto last_time = std::chrono::steady_clock::now();
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        auto now = std::chrono::steady_clock::now();
        std::lock_guard<std::mutex> lock(interval_mutex);
        if (std::chrono::duration_cast<std::chrono::seconds>(now - last_time).count() >= servus_interval) {
            std::cout << "Servus" << std::endl;
            last_time = now;
        }
    }
}

void readInput() {
    while (true) {
        int new_hello, new_servus;
        std::cin >> new_hello >> new_servus;
        std::lock_guard<std::mutex> lock(interval_mutex);
        hello_interval = new_hello;
        servus_interval = new_servus;
    }
}

int main() {
    std::thread helloThread(printHello);
    std::thread servusThread(printServus);
    std::thread inputThread(readInput);

    helloThread.join();
    servusThread.join();
    inputThread.join();

    return 0;
}
