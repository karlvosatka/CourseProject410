import javafx.application.Application;

import javafx.application.Platform;
import javafx.beans.Observable;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;

import javafx.scene.control.*;
import javafx.scene.input.DragEvent;
import javafx.scene.input.TransferMode;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.logging.Handler;

public class JavaFXTemplate extends Application {



	HashMap<String, Scene> scenes;

	ColorTuple primaryColor;
	ColorTuple secondaryColor;
	String font;
	ProgramRunner runThread;

	// Color Tuple
	//
	// Internal class that is used to help store the colors properly which will aid
	// with making color changes simple and easy
	public class ColorTuple {
		public String colorName;
		public Color color;

		// ColorTuple constructor that initializes the data members of the class.
		public ColorTuple(String name, Color color) {
			colorName = name;
			this.color = color;
		}
	}



	public static void main(String[] args) {
		// TODO Auto-generated method stub
		launch(args);
	}

	//feel free to remove the starter code from this method
	@Override
	public void start(Stage primaryStage) throws Exception {
		// TODO Auto-generated method stub
		primaryStage.setTitle("Welcome to JavaFX");
		scenes = new HashMap<String, Scene>();
		font = "Baskerville";
		primaryColor = new ColorTuple("CADETBLUE", Color.CADETBLUE);
		secondaryColor = new ColorTuple("BURLYWOOD", Color.BURLYWOOD);

		scenes.put("Start", buildStartScreen(primaryStage));
		scenes.put("Wait", buildWaitingScreen());
		primaryStage.setScene(scenes.get("Start"));
		primaryStage.show();
	}


	// Builds the launch screen for the programs that I wrote
	//
	public Scene buildStartScreen(Stage primaryStage)
	{
		BorderPane borderPane = new BorderPane();
		borderPane.setPadding(new Insets(20));



		// middle
		VBox center = new VBox(45);
		center.setAlignment(Pos.CENTER);

		Label title = new Label("Welcome to our Project");
		title.setStyle("-fx-font-size: 45");
		title.setBackground(
				new Background(new BackgroundFill(secondaryColor.color, new CornerRadii(0), new Insets(-7))));

		TextField url = new TextField();

		HBox buttons = new HBox(30);
		buttons.setAlignment(Pos.CENTER);

		Button run = new Button("Run");
		run.setStyle("-fx-font-size: 30; -fx-border-color: black; -fx-background-color: salmon");
		run.setOnAction(e->{
			((Button) e.getSource()).setDisable(true);
			runThread = new ProgramRunner(url.getText(), signal->{
				Platform.runLater(()->{
					primaryStage.setScene(scenes.get(signal));
				});
			});
			runThread.start();
		});

//		use this if you want the user to change the theme of the program (In particular the background)
//		run.setBackground(
//				new Background(new BackgroundFill(Color.SALMON, new CornerRadii(0), new Insets(0))));

		run.setDisable(true);

		run.setOnMouseEntered(e -> run.setStyle("-fx-font-size: 30; -fx-border-color: black; -fx-background-color: green"));
		run.setOnMouseExited(e -> run.setStyle("-fx-font-size: 30; -fx-border-color: black; -fx-background-color: salmon"));

		url.setPromptText("Enter URL Here");
		url.setOnKeyTyped(e->{
			if(url.getText().equals("")) {
				run.setDisable(true);
			}
			else {
				run.setDisable(false);
			}
		});


		center.getChildren().addAll(title, url, run);

		borderPane.setCenter(center);

		borderPane.setStyle(
				"-fx-background-color: " + primaryColor.colorName + "; -fx-border-width: 10; -fx-border-color: "
						+ secondaryColor.colorName + "; -fx-font-family: " + font);

		return new Scene(borderPane, 700, 700);
	}

	public Scene buildWaitingScreen()
	{
		VBox contents = new VBox(80);
		contents.setAlignment(Pos.CENTER);
		contents.setStyle("-fx-background-color: " + primaryColor.colorName + "; -fx-border-width: 10; -fx-border-color: "
				+ secondaryColor.colorName + "; -fx-font-family: " + font);

		Label waitPrompt = new Label("Waiting for program to finish...");
		waitPrompt.setStyle("-fx-font-size: 24");
		waitPrompt.setBackground(new Background(new BackgroundFill(secondaryColor.color, new CornerRadii(0), new Insets(-7))));
		waitPrompt.setAlignment(Pos.TOP_CENTER);

		contents.getChildren().addAll(waitPrompt);

		return new Scene(contents, 700, 700);
	}

}
