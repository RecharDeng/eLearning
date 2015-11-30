#pragma once
#include <memory>
#include <vector>
#include <functional>
#include <condition_variable>
#include <thread>
using std::unique_ptr;
using std::vector;
using std::function;
using std::mutex;

template<typename T>
class ObjectPool
{
    using deleter = std::function<void(T*)>;
public:
    ObjectPool() = default;
    ~ObjectPool() = default;

    void addObject(unique_ptr<T> objPtr)
    {
        std::unique_lock<std::mutex> ul(objObtainLock);
        objCont.emplace_back(std::move(objPtr));
    }

    unique_ptr<T, deleter> get()
    {
        std::unique_lock<std::mutex> ul(objObtainLock);
        if (objCont.empty())
            throw std::logic_error("no more objects");

        auto objPtr = unique_ptr<T, deleter>(objCont.back().release(), [this](T* obj)
        {
            std::unique_lock<std::mutex> ul(objObtainLock);
            objCont.emplace_back(obj);
        });
        objCont.pop_back();
        return objPtr;
    }          

    bool hasMoreObject() const
    {
        return !objCont.empty();
    }

    size_t objectsRemained() const
    {
        return objCont.size();
    }                         

private:
    vector<unique_ptr<T>> objCont;   
    static std::mutex objObtainLock;
};
template<typename T> 
std::mutex ObjectPool<T>::objObtainLock;

