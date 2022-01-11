import 'package:flutter/material.dart';

class BookPage extends StatelessWidget {
  const BookPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
    return Scaffold(
      resizeToAvoidBottomInset : false,
      appBar: AppBar(
        title: const Text('Add a book'),
      ),
      body: Center(
        child: Column(
          children: [
            Form(
              key: _formKey, child: Column(
              children: <Widget>[
                Padding(padding: const EdgeInsets.fromLTRB(15, 30, 15, 0),
                child:
                TextFormField(
                  decoration: const InputDecoration(
                    hintText: 'Enter the book name',
                  ),
                  validator: (String? value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter some text';
                    }
                    return null;
                  },
                ),
                ),

                Padding(
                  padding: const EdgeInsets.fromLTRB(10, 30, 10, 10),
                  child: ElevatedButton(
                    onPressed: () {
                      // Validate will return true if the form is valid, or false if
                      // the form is invalid.
                      if (_formKey.currentState!.validate()) {
                        // Process data.
                      }
                    },
                    child: const Text('Submit'),
                  ),
                ),
              ],
            ),

            ),
            ElevatedButton(
                child: const Text('Go back'),
                onPressed: () {
                  Navigator.pop(context);
                }
            ),
          ],
        )
      ),
    );
  }
}