import 'package:flutter/material.dart';
import 'community/community_screen.dart';
import 'home/home_screen.dart';
import 'profile/profile_screen.dart';
import 'contants/contants_screen.dart';

class YoungMainScreen extends StatefulWidget {
  const YoungMainScreen({super.key});

  @override
  State<YoungMainScreen> createState() => _YoungMainScreenState();
}

class _YoungMainScreenState extends State<YoungMainScreen> {
  int _selectedIndex = 0; // 현재 인덱스

  /* 메뉴 탭 화면 이동 함수*/
  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
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
      /* 화면 */
      body: IndexedStack(
        index: _selectedIndex,
        children: const [
          HomeScreen(), // 홈 화면
          StoryScreen(), // 이야기 화면
          CommunityScreen(), // 커뮤니티 화면
          ProfileScreen(),
        ],
      ),

      /* 네비게이션 메뉴 */
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed, //메뉴 4개 이상
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.menu_book_rounded),
            label: '컨텐츠',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.forum_outlined),
            label: '커뮤니티',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_circle),
            label: '나의 발자취',
          ),
        ],
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }
}
