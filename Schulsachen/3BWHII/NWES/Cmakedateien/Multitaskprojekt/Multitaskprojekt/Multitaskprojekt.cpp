// Multitasking.cpp: Definiert den Einstiegspunkt für die Anwendung.
//

// Multitasking.cpp: Defines the entry point for the application.
//

#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <semaphore>
#include <map>


bool isPrime(int num) {
    if (num <= 1) return false;
    if (num <= 3) return true;
    if (num % 2 == 0 || num % 3 == 0) return false;
    for (int i = 5; i * i <= num; i += 6) {
        if (num % i == 0 || num % (i + 2) == 0) return false;
    }
    return true;
}

std::counting_semaphore semaphore(1);

bool running = true;
std::mutex count_mutex;

void ThreadFunction(std::string ThreadName)
{
    while (running)
    {
        count_mutex.lock();
        std::cout << "Thread: " << ThreadName << " is running" << std::endl;
        count_mutex.unlock();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int intervall = 2000000;
std::map<int, bool> is_prime;

void prime_thread_function(int start_value)
{
    for (int i = start_value; i < (start_value + intervall); i++)
    {
        bool is_prime_ = isPrime(i);
        is_prime[i] = is_prime_;

    }
}


int main()
{
    std::map<int, bool> is_prime;
    auto startzeit = std::chrono::system_clock::now();
    std::thread t1(prime_thread_function, 0);
    std::thread t2(prime_thread_function, 2000000);
    std::thread t3(prime_thread_function, 4000000);
    std::thread t4(prime_thread_function, 6000000);
    std::thread t5(prime_thread_function, 8000000);

    t1.join();
    t2.join();
    t3.join();
    t4.join();
    t5.join();

    auto endzeit = std::chrono::system_clock::now();
    auto zeitspanne = std::chrono::duration_cast<std::chrono::milliseconds>
        (endzeit - startzeit);
    std::cout << "Berechnung hat "
        << zeitspanne.count()
        << "gedauert" << std::endl;

    return 0;

}