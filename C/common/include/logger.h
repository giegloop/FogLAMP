#ifndef _LOGGER_H
#define _LOGGER_H
/*
 * FogLAMP storage service.
 *
 * Copyright (c) 2017-2018 OSisoft, LLC
 *
 * Released under the Apache 2.0 Licence
 *
 * Author: Mark Riddoch, Massimiliano Pinto
 */

#include <string>

#define PRINT_FUNC	Logger::getLogger()->info("%s:%d", __FUNCTION__, __LINE__);
#define PRINT_FUNC_DONE	Logger::getLogger()->info("%s:%d done", __FUNCTION__, __LINE__);

#define START_TIME std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
#define END_TIME std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now(); \
				 auto usecs = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
#define PRINT_TIME(msg) std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now(); \
				 auto usecs = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count(); \
				 Logger::getLogger()->info("%s:%d: " msg " took %lld usecs", __FUNCTION__, __LINE__, usecs);

/**
 * FogLAMP Logger class used to log to syslog
 *
 * At startup this class should be constructed
 * using the standard constructor. To log a message
 * call debug, info, warn etc. using the instance
 * of the class. TO get that instance call the static
 * method getLogger.
 */
class Logger {
	public:
		Logger(const std::string& application);
		~Logger();
		static Logger *getLogger();
		void debug(const std::string& msg, ...);
		void info(const std::string& msg, ...);
		void warn(const std::string& msg, ...);
		void error(const std::string& msg, ...);
		void fatal(const std::string& msg, ...);
		void setMinLevel(const std::string& level);
	private:
		std::string 	*format(const std::string& msg, va_list ap);
		static Logger   *instance;
		std::string 	*m_app_name;
};

#endif
