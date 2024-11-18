import 'package:flutter/material.dart';
import 'package:flutter_settings_screens/flutter_settings_screens.dart';

class ElderProfileSceen extends StatefulWidget {
  const ElderProfileSceen({super.key});

  @override
  State<ElderProfileSceen> createState() => _ElderProfileSceenState();
}

class _ElderProfileSceenState extends State<ElderProfileSceen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('설정'),
        centerTitle: false,
      ),
      body: ListView(
        children: [
          // 알림 설정

          const ListTile(
            title: Text('알림 설정'),
          ),

          const Divider(),

          // 사용자 설정
          const ListTile(
            title: Text('사용자 설정'),
          ),
          ListTile(
            title: const Text('계정 / 정보 관리'),
            onTap: () {
              // 계정/정보 관리 화면으로 이동
            },
          ),
          ListTile(
            title: const Text('기타 설정'),
            onTap: () {
              // 기타 설정 화면으로 이동
            },
          ),
          const Divider(),

          // 기타
          const ListTile(
            title: Text('기타'),
          ),
          ListTile(
            title: const Text('공지사항'),
            onTap: () {
              // 공지사항 화면으로 이동
            },
          ),
          ListTile(
            title: const Text('언어 설정'),
            onTap: () {
              // 언어 설정 화면으로 이동
            },
          ),
          ListTile(
            title: const Text('캐시 데이터 삭제'),
            onTap: () {},
          ),
          ListTile(
            title: const Text('로그아웃'),
            onTap: () {},
          ),
          ListTile(
            title: const Text('탈퇴하기'),
            onTap: () {},
          ),
        ],
      ),
    );
  }
}
