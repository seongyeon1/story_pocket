import 'package:flutter/material.dart';
import '../../../widgets/search_bar.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SizedBox.expand(
        // 부모 위젯 너비 최대값 설정
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                //검색바
                alignment: Alignment.center,
                child: SearchBarForStories(
                  trailing: [
                    IconButton(
                      onPressed: () {},
                      icon: const Icon(Icons.keyboard_voice),
                    ),
                    IconButton(
                      onPressed: () {},
                      icon: const Icon(Icons.search),
                    ),
                  ],
                ),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
              const Text(
                "sdfsdf",
                style: TextStyle(fontSize: 40),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
