import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../models/story.dart';
import '../../common/widgets/menu_tile.dart';
import 'elder_community_detail_screen.dart';

class ElderCommunityScreen extends StatefulWidget {
  const ElderCommunityScreen({super.key});

  @override
  State<ElderCommunityScreen> createState() => _ElderCommunityScreenState();
}

class _ElderCommunityScreenState extends State<ElderCommunityScreen> {
  List<Story> stories = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchStories();
  }

  // API에서 데이터 가져오기
  Future<void> fetchStories() async {
    try {
      final response = await http.get(Uri.parse("http://localhost:8000/api/stories")); // 백엔드 API URL
      if (response.statusCode == 200) {
        // UTF-8 디코딩 추가
        final List<dynamic> storyList = json.decode(utf8.decode(response.bodyBytes));
        setState(() {
          stories = storyList.map((data) => Story.fromJson(data)).toList();
          isLoading = false;
        });
      } else {
        throw Exception("Failed to load stories");
      }
    } catch (e) {
      print("Error fetching stories: $e");
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("이야기 구경하기"),
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
      body: isLoading
          ? const Center(child: CircularProgressIndicator()) // 로딩 상태 표시
          : ListView.separated(
              itemCount: stories.length,
              itemBuilder: (context, index) {
                final story = stories[index];
                final order = index;
                // 타일 위젯
                Widget storyScreen = ElderCommunityDetailScreen(story: story);
                return buildStoryTile(story, order, context, storyScreen);
              },
              separatorBuilder: (BuildContext context, int index) {
                return const Divider();
              },
            ),
    );
  }
}