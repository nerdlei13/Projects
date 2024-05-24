import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

class PasswordManagerV2 {
	
	private static String USERNAME = "joebob";
	private static String PASSWORD = "PassWord123";
    private Map<String, String> userMap;

	public static void main(String[] args) {
		PasswordManagerV2 v2 = new PasswordManagerV2();
        v2.passwordManagerV2();
	}

    public PasswordManagerV2() {
        this.userMap = new HashMap<>();
        userMap.put(USERNAME, PASSWORD);
        userMap.put("bbjean", "123Abc");
    }

	private boolean validateUserNameAndPassword(String username, String password) {
		return userMap.containsKey(username) && userMap.get(username).equals(password);
	}

	public void passwordManagerV2() {
		boolean hasValidCredentials = true;
		Scanner scanner = new Scanner(System.in);

		while (hasValidCredentials) {
			System.out.println("Enter user name: ");
			String inputUserName = scanner.nextLine();
			System.out.println("Enter password: ");
			String inputUserPassword = scanner.nextLine();

			if (validateUserNameAndPassword(inputUserName, inputUserPassword)) {
				System.out.println("Credentials accepted!\n");
				System.out.println("Secret is: You got this :) \n");
				scanner.close();
				hasValidCredentials = false;
			} else {
				System.out.println("Invalid username or password. Please try again:");
			}
			
		}
	}
}