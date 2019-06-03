using M2MqttUnity.Examples;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.XR.WSA.Input;

public class WorldCursor : MonoBehaviour {

    // Use this for initialization
    private MeshRenderer meshRenderer;
    public static WorldCursor Instance { get; private set; }

    // Represents the hologram that is currently being gazed at.
    public GameObject FocusedObject { get; private set; }

    GestureRecognizer recognizer;
    public delegate void ClickAction(Vector3 pos);
    public static event ClickAction OnClicked;

    public delegate void TabAction1(Vector3 pos);
    public static event TabAction1 OnTabSetup1;

    public delegate void TabAction2(Vector3 pos);
    public static event TabAction2 OnTabSetup2;

    public delegate void ResetAction();
    public static event ResetAction ResetWorld;

    public Vector3 LeftUp { get; set; }
    public Vector3 RightDown { get; set; }
    private int CountCalibration;
    private bool SetupRun;
    KeywordRecognizer keywordRecognizer = null;
    Dictionary<string, System.Action> keywords = new Dictionary<string, System.Action>();

    public double procentX { get; set; }
    public double procentY { get; set; }

    void OnEnable()
    {
        M2MqttUnityTest.Message += SetXY;


    }


    void OnDisable()
    {
        M2MqttUnityTest.Message -= SetXY;
        //unsubscribe op het event
    }

    // Use this for initialization
    void Start()
    {
        // Grab the mesh renderer that's on the same object as this script.
        meshRenderer = this.gameObject.GetComponentInChildren<MeshRenderer>();
        CountCalibration = 0;
        SetupRun = true;
        procentX = 0.5;
        procentY = 0.5;

        keywords.Add("Reset", () =>
        {
            Debug.Log("reset");
            if (ResetWorld != null)
                ResetWorld();
            CountCalibration = 0;
            SetupRun = true;


        });


        // Tell the KeywordRecognizer about our keywords.
        keywordRecognizer = new KeywordRecognizer(keywords.Keys.ToArray());

        // Register a callback for the KeywordRecognizer and start recognizing!
        keywordRecognizer.OnPhraseRecognized += KeywordRecognizer_OnPhraseRecognized;
        keywordRecognizer.Start();
    }
    void Awake()
    {
        Instance = this;

        // Set up a GestureRecognizer to detect Select gestures.
        recognizer = new GestureRecognizer();
        recognizer.Tapped += (args) =>
        {



            if (SetupRun)
            {
                CountCalibration++;
            }

            switch (CountCalibration)
            {
                case 1:
                    LeftUp = this.transform.position;
                    

                    if (OnTabSetup1 != null)
                        OnTabSetup1(LeftUp);

                    break;
                case 2:
                    RightDown = this.transform.position;

                    if (OnTabSetup2 != null)
                        OnTabSetup2(RightDown);
                    CountCalibration = 0;
                    SetupRun = false;


                    break;
                default:
                    break;
            }

            // Send an OnSelect message to the focused object and its ancestors.





        };
        recognizer.StartCapturingGestures();
    }


    // Update is called once per frame
    void Update()
    {
        if (SetupRun == false)
        {
            CalcPlane(procentX, procentY);
        }

        // Do a raycast into the world based on the user's
        // head position and orientation.
        var headPosition = Camera.main.transform.position;
        var gazeDirection = Camera.main.transform.forward;

        RaycastHit hitInfo;

        if (Physics.Raycast(headPosition, gazeDirection, out hitInfo))
        {
            // If the raycast hit a hologram...
            // Display the cursor mesh.
            meshRenderer.enabled = true;

            // Move the cursor to the point where the raycast hit.
            this.transform.position = hitInfo.point;

            // Rotate the cursor to hug the surface of the hologram.
            this.transform.rotation = Quaternion.FromToRotation(Vector3.up, hitInfo.normal);
        }
        else
        {
            // If the raycast did not hit a hologram, hide the cursor mesh.
            meshRenderer.enabled = false;
        }
    }
    void CalcPlane(double ProcentX, double ProcentY)
    {

        float Lenght = RightDown.x - LeftUp.x;

        float Height = LeftUp.z - RightDown.z;

        Vector3 TeleportPos;
        TeleportPos.x = (float)(Lenght * ProcentX) + LeftUp.x;
        TeleportPos.z = (float)(LeftUp.z - (Height * ProcentY));
        TeleportPos.y =(float)(LeftUp.y+0.1);
        if (OnClicked != null)
            OnClicked(TeleportPos);


    }

    private void KeywordRecognizer_OnPhraseRecognized(PhraseRecognizedEventArgs args)
    {
        System.Action keywordAction;
        if (keywords.TryGetValue(args.text, out keywordAction))
        {
            keywordAction.Invoke();
        }
    }

    public void SetXY(double X, double Y)
    {
        procentX = X;
        procentY = Y;
    }
}
