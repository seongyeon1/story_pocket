import 'package:flutter/material.dart';

class TalkScreen extends StatefulWidget {
  const TalkScreen({super.key});

  @override
  State<TalkScreen> createState() => _TalkScreenState();
}

class _TalkScreenState extends State<TalkScreen> {
  final speech_balloon_text =
      const TextStyle(fontSize: 17, fontWeight: FontWeight.w600);

  void _popTalkScreen() {
    // TODO: 이야기 하기 화면으로 이동하는 로직 구현
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.monetization_on_rounded),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.notifications),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.account_circle_rounded),
          )
        ],
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center, // 중앙
        children: [
          /* 텍스튼 */
          Container(
            alignment: const Alignment(0, 0),
            child: const Text("마이크 버튼을 클릭하고 대화를 나눠보세요!"),
          ),
          const SizedBox(
            height: 20,
          ),

          /* 말풍선 */
          Stack(
            children: [
              Image.asset(
                'assets/image/speech_balloon.png',
                height: 200,
              ),
              Positioned(
                top: 50,
                left: 70,
                child: SizedBox(
                  child: Column(
                    children: [
                      Text(
                        "할머니 할아버지",
                        style: speech_balloon_text,
                      ),
                      Text(
                        "재밌는 이야기 해주세요!",
                        style: speech_balloon_text,
                      ),
                    ],
                  ),
                ),
              )
            ],
          ),

          /* 소녀이미지 */
          Image.asset(
            'assets/image/girl.png',
            height: 300,
          ),

          /* 마이크 버튼 */
          Container(
            decoration: const ShapeDecoration(
              shape: CircleBorder(
                side: BorderSide(color: Colors.black, width: 2),
              ),
            ),
            child: IconButton(
              onPressed: () {},
              icon: const Icon(
                Icons.mic_outlined,
                size: 45,
              ),
            ),
          ),
          const SizedBox(
            height: 20,
          ),

          /* 뒤로가기 버튼 */
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              fixedSize: const Size.fromWidth(199),
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
            onPressed: _popTalkScreen,
            child: const Text(
              "뒤로가기",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w700,
              ),
            ),
          )
        ],
      ),
    );
  }
}
