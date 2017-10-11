/*
* This is the Read Write Lock
* wyf 20171011
*/
#ifndef __RWLOCK_HH__
#define __RWLOCK_HH__
#if _MSC_VER > 1000
#pragma once
#endif
#include <boost/thread.hpp>
#include <boost/noncopyable.hpp>

namespace wyf
{
	class rwlock:boost::noncopyable
	{
	protected:
		boost::mutex mutex_;
		boost::condition_variable_any read_allowed_condition_;
		boost::condition_variable_any write_allowed_condition_;
		bool m_writelocked_;
		uint32_t m_readlocked_;

	public:
		rwlock() :
			m_writelocked_(false), 
			m_readlocked_(0)
		{}
		friend class scoped_read_lock;
		friend class scoped_write_lock;
	private:
		void ReadLock()
		{
			boost::mutex::scoped_lock lock_(mutex_);
			while (m_writelocked_)
			{
				read_allowed_condition_.wait(mutex_);
			}
			++m_readlocked_;
		}

		void ReadUnlock()
		{
			boost::mutex::scoped_lock lock_(mutex_);
			--m_readlocked_;
			if (m_readlocked_ == 0)
			{
				write_allowed_condition_.notify_all();
			}
		}

		void WriteLock()
		{
			boost::mutex::scoped_lock lock_(mutex_);
			while (m_readlocked_ != 0 || m_writelocked_)
				write_allowed_condition_.wait(mutex_);
			m_writelocked_ = true;
		}

		void WriteUnlock()
		{
			boost::mutex::scoped_lock lock_(mutex_);
			m_writelocked_ = false;
			write_allowed_condition_.notify_all();
			read_allowed_condition_.notify_all();
		}

	public:
		class scoped_read_lock
		{
		private:
			rwlock& rwlocker_;
		public:
			scoped_read_lock(rwlock& rwlocker__) :
				rwlocker_(rwlocker__)
			{
				rwlocker_.ReadLock();
			}

			~scoped_read_lock()
			{
				rwlocker_.ReadUnlock();
			}
		};

		class scoped_write_lock
		{
		private:
			rwlock& rwlocker_;
		public:
			scoped_write_lock(rwlock& rwlocker__) :
				rwlocker_(rwlocker__)
			{
				rwlocker_.WriteLock();
			}

			~scoped_write_lock()
			{
				rwlocker_.WriteUnlock();
			}
		};
	};

};








#endif