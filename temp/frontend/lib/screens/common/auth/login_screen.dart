import 'package:flutter/material.dart';
import '../../elder/elder_main_screen.dart';
import '../../young/young_main_screen.dart';

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

  /* 65세 미만 MainScreen으로 이동 */
  void _navigateToMainScreen() {
    Navigator.pushReplacement(
      //이전 페이지 스택에서 제거
      context,
      MaterialPageRoute(builder: (context) => const YoungMainScreen()),
    );
  }

  /* 65세 이상MainScreen으로 이동 */
  void _navigateToElderMainScreen() {
    Navigator.pushReplacement(
      //이전 페이지 스택에서 제거
      context,
      MaterialPageRoute(builder: (context) => const ElderMainScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/image/loginpage_background.png'),
            fit: BoxFit.cover, //사진 비율 유지
          ),
        ),
        child: Stack(
          children: [
            /* sub TItle */
            Align(
              alignment: const Alignment(-1.1, -0.6),
              child: Image.asset(
                'assets/image/login_sub_title.png',
                width: 200,
              ),
            ),
            /* 제목 */
            Align(
              alignment: const Alignment(0, -0.30), //위로 35%
              child: Image.asset(
                'assets/image/login_page_title.png',
                width: 300,
              ),
            ),
            /* 로그인 버튼 */
            Align(
              alignment: const Alignment(0, 0.6),
              child: ElevatedButton(
                style: _startButtonStyle,
                onPressed: _navigateToMainScreen,
                child: Text(
                  "이야기 시작하기",
                  style: _startStyle,
                ),
              ),
            ),
            /* (임시) 65세 로그인 */
            Align(
              alignment: const Alignment(0, 0.7),
              child: TextButton(
                onPressed: _navigateToElderMainScreen,
                child: const Text(
                  "65세 이상",
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 15,
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
