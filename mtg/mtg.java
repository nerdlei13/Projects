import java.util.HashMap;
import java.util.Scanner;
public class MTG{
    public static void main(String [] args){
     isValidInput();
        
    }

    public static String isValidInput(){
        Scanner console = new Scanner(system.in);
        System.out.print("Enter a sequence: ");
        console.nextLine();

        String valid = console.nextLine();
        while(valid.hasNextLine())
        {
         System.out.print("Enter a valid string: ");
         valid.nextLine();
         while(valid.length() >= 1 || valid.length() < 5)
         {
            console.nextLine();
            System.out.print("Enter a valid string: ");
         }
         valid = console.nextLine();
      }
        return valid;
    }
    /*public static String isAnagram(String valid){

    }*/

    public static void fillMap(){
        HashMap<String, String> map = new HashMap<String, String>();
        File file = new File("keys.txt");
        Scanner input = new Scanner(file);
        int colon = input.indexOf(":");
        while(input.hasNextLine()){
            String token = input.nextLine();
            String key = token.substring(0, colon);
            String value = token.substring(colon);
            map.put(key,value);
        } 
    }
}

