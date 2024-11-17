import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';
import 'package:my_project/data/story_dummy_data.dart';
import 'package:my_project/screens/common/widgets/story_tile.dart';
import 'package:my_project/screens/elder/storybook/elder_storybook_defail_screen.dart';

class ElderStoybookScreen extends StatefulWidget {
  const ElderStoybookScreen({super.key});

  @override
  State<ElderStoybookScreen> createState() => _ElderStoybookScreenState();
}

class _ElderStoybookScreenState extends State<ElderStoybookScreen> {
  //동화 데이터 리스트 저장 변수
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
        title: const Text("동화책"),
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
      //동화 리스트
      body: ListView.separated(
        itemCount: storyData.length,
        itemBuilder: (context, index) {
          final story = stories[index];
          final order = index;
          //타일 위젯
          Widget storyScreen = ElderStorybookDefailScreen(story: story);
          return buildStoryTile(story, order, context, storyScreen);
        },
        separatorBuilder: (BuildContext context, int index) {
          return const Divider();
        },
      ),
    );
  }
}
