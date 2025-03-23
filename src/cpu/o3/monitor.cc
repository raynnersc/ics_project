#include "cpu/o3/monitor.hh"
#include "cpu/o3/dyn_inst.hh"

namespace gem5
{

namespace o3
{

Monitor::Monitor()
{
    rob = nullptr;
    std::string filename = "/home/infres/rcarvalho-23/gem5/m5out/data.txt";
    outfile.open(filename);
    outfile << "Tick \t nInstrInROB \t nFin \t nRun \t nWaiting" << std::endl;
}

Monitor::~Monitor()
{
    outfile.close();
}

void
Monitor::setROB(ROB *rob_ptr)
{ 
    rob = rob_ptr; 
    std::cout << "Monitor ROB pointer: " << rob << std::endl;
}

void
Monitor::saveStats(int tick, int n, int nFinInstr, int nRun, int nWaiting)
{
    if(!outfile)
    {
        std::cerr << "Error to open the DATA file!" << std::endl;
        return;
    }

    outfile << tick << "\t" << n << "\t" << nFinInstr << "\t" << nRun << "\t" << nWaiting << std::endl;
}

void
Monitor::tick()
{
    int tick = curTick();
    int n = rob->numInstsInROB;
    int nReadyToCommit = 0;
    int nIssued = 0;
    int nWaiting = 0;

    ThreadID tid = 0;
    const std::list<DynInstPtr>& instList = rob->getInstList(tid);

    for(auto it = instList.cbegin(); it != instList.cend(); it++)
    {
        // Instructions executed
        if ((*it)->readyToCommit())
            nReadyToCommit++;
        // Instructions executing
        else if ((*it)->isIssued())
            nIssued++;
        // Instructions waiting dependencies
        else if ((*it)->isInIQ() && !(*it)->readyToIssue())
            nWaiting++;
    }

    saveStats(tick, n, nReadyToCommit, nIssued, nWaiting);
}

} // namespace o3
} // namespace gem5