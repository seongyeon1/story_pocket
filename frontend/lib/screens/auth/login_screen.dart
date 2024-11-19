import 'package:flutter/material.dart';
import 'package:my_project/screens/auth/id_pw_screen.dart';
import '../contants/elder_main_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  /* 로그인 버튼 텍스트 스타일 */
  final TextStyle _startStyle = const TextStyle(
    fontSize: 19,
    color: Colors.black,
    fontWeight: FontWeight.w800,
  );

  /* 버튼스타일 */
  final ButtonStyle _startButtonStyle = ButtonStyle(
    fixedSize: WidgetStateProperty.all(
      const Size(230, 50),
    ),
  );

  /* 로그인 페이지로 이동 */
  void _navigateToLoginPage() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const IdPwScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/image/login/loginpage_background.png'),
            fit: BoxFit.cover, //사진 비율 xw유지
          ),
        ),
        child: Stack(
          children: [
            /* sub TItle */
            Align(
              alignment: const Alignment(-1.1, -0.6),
              child: Image.asset(
                'assets/image/login/login_sub_title.png',
                width: 200,
              ),
            ),
            /* 제목 */
            Align(
              alignment: const Alignment(0, -0.30), //위로 35%
              child: Image.asset(
                'assets/image/login/login_page_title.png',
                width: 300,
              ),
            ),
            /* 로그인 버튼 */
            Align(
              alignment: const Alignment(0, 0.6),
              child: IconButton(
                icon: Image.asset(
                  "assets/image/login/naver_login.png",
                  width: 200,
                ),
                onPressed: () {},
              ),
            ),
            Align(
              alignment: const Alignment(0, 0.73),
              child: IconButton(
                icon: Image.asset(
                  "assets/image/login/kakao_login.png",
                  width: 200,
                ),
                onPressed: () {},
              ),
            ),

            /* (임시) 65세 로그인 */
            Align(
              alignment: const Alignment(0, 0.80),
              child: TextButton(
                onPressed: _navigateToLoginPage,
                child: const Text(
                  "이메일로 로그인하기",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
