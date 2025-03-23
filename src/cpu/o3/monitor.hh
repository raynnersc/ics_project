#ifndef __CPU_O3_MONITOR_HH__
#define __CPU_O3_MONITOR_HH__

#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include "cpu/o3/rob.hh"

namespace gem5
{

namespace o3
{

class ROB;
    
class Monitor
{
    private:
        ROB *rob;
        std::ofstream outfile;
    public:
        Monitor();
        ~Monitor();
        void tick();
        void setROB(ROB *rob_ptr);
        void saveStats(int tick, int n, int nFinInstr, int nRun, int nWaiting);
};

} // namespace o3
} // namespace gem5

#endif // __CPU_O3_MONITOR_HH__