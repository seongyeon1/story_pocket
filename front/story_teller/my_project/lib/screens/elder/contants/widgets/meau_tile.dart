import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';
import 'package:my_project/screens/elder/contants/elder_story_detail_screen.dart';

Widget buildStoryTile(Story story, int order, BuildContext context) {
  return ListTile(
    leading: const CircleAvatar(
      backgroundImage: AssetImage("assets/image/grandma_grandpa.png"),
    ),
    title: Text(story.title),
    trailing: Column(
      children: [
        Text('조회수: ${story.numberOfView}'),
        Text('작성자: ${story.author}')
      ],
    ),
    onTap: () {
      //상세 이야기 화면
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ElderStoryDetailScreen(story: story),
        ),
      );
    },
  );
}
