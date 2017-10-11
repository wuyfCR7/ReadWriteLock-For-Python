#include "RWLock.hh"
#include <iostream>
#include <boost/timer.hpp>
#pragma comment(lib, "libboost_thread-vc120-mt-gd-1_58.lib")
int val_ = 0;
boost::mutex cout_mutex_;
wyf::rwlock rwlock_;
/// boost::shared_mutex rwlock_;
void readfcn()
{
	for (int t = 0; t < 200; ++t)
	{
		{
			wyf::rwlock::scoped_read_lock lock_(rwlock_);
			/// boost::shared_lock<boost::shared_mutex> lock_(rwlock_);
			int val__ = ::val_;
		}
		{
			boost::mutex::scoped_lock lock__(cout_mutex_);
			std::cout << boost::this_thread::get_id() << "\t" << val_ << std::endl;
		}
		boost::this_thread::sleep_for(boost::chrono::milliseconds(20));
	}
}
void writefcn()
{
	for (int t = 0; t < 200; ++t)
	{
		{
			wyf::rwlock::scoped_write_lock lock_(rwlock_);
			/// boost::unique_lock<boost::shared_mutex> lock_(rwlock_);
			++val_;
		}
		boost::this_thread::sleep_for(boost::chrono::milliseconds(10));
	}
}
int main()
{
	boost::timer timer_;
	boost::thread_group group_;
	for (int t = 0; t < 5; ++t)
		group_.create_thread(readfcn);
	for (int t = 0; t < 12; ++t)
		group_.create_thread(writefcn);
	for (int t = 0; t < 5; ++t)
		group_.create_thread(readfcn);

	group_.join_all();
	std::cout << timer_.elapsed() << " s" << std::endl;
	system("pause");
	return NULL;
}