import java.util.*;
public class SS {
    public static boolean prime(int num) {
        for(int i = 2; i <= num/2; i++) {
            if(num%i==0){
                return false;
            }
        }
        return true;
    }
    public static void main(String[] args) {
       Scanner sc = new Scanner(System.in);
       int n  = sc.nextInt();
       int c = 0;
       int p = 2;
       while(true) {
            if(prime(p) == true) {
                c++;
            }
            n--;
            p++;
            if(p == c) {
                break;
            }
       }
    }
}