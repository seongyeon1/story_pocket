import 'package:flutter/material.dart';
import '../../../data/community_dummy_data.dart';
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

  @override
  void initState() {
    // TODO: implement initState

    // 데이터 가져오기
    super.initState();
    stories = storyData
        .map((data) => Story(
              title: data['title'] as String,
              author: data['author'] as String,
              story: data['story'] as String,
              numberOfView: data['numberOfView'] as int,
            ))
        .toList();
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
      body: ListView.separated(
        itemCount: storyData.length,
        itemBuilder: (context, index) {
          final story = stories[index];
          final order = index;
          //타일 위젯
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
