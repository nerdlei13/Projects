#include <string>




namespace cpp_practice {
class passwordManager {
    public:
        passwordManager() {};
        bool validateUserNameAndPassword(const std::string& username, const std::string& password);
        
        void accessCredentials();
    
    private:
        const std::string USERNAME = "joebob";
        const std::string PASSWORD = "PassWord123";

};

}

