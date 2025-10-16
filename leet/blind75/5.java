//https://leetcode.com/problems/longest-palindromic-substring/?envType=problem-list-v2&envId=oizxjoit
class Solution {
 // public static String s = "abad";

    public static boolean isPalindrome(String s) {
        int len = s.length();
        for (int i = 0; i < len; i++) {
            if (s.charAt(i) != s.charAt(len - 1 - i)) {
                return false;
            }

        }
        return true;
    }

     public static String longestPalindrome(String s) {
        int max = 0;
        // make combinations of windows
        String result=  "";
        if (s.length() == 1){
            return s;
        }

        for (int win_size=0 ; win_size< s.length(); win_size++){
            for (int start = 0 ; start < (s.length() - win_size); start++){
                String subs = s.substring(start, start+win_size+1);
                // System.out.println(subs);
                // System.out.println(s.substring(0, 2));
                 if (isPalindrome(subs)){
                    if (subs.length() > max){
                       max= subs.length();
                       result =subs;
                       break;
                    }
                    }
        // if is palindrome then compare to max
        // if bigger than max, assign
            }
        }

        

       
      //  System.out.println(result);
        return result;

    }
}