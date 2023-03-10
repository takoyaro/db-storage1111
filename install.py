import launch

if not launch.is_installed("pymongo"):
    launch.run_pip("install pymongo", "requirements for mongo-storage")