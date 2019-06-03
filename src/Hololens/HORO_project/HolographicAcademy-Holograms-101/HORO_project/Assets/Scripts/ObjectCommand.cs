using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.WSA.Input;

public class ObjectCommand : MonoBehaviour {

    // Use this for initialization
    public static ObjectCommand Instance { get; private set; }
    

    // Represents the hologram that is currently being gazed at.
    public GameObject FocusedObject { get; private set; }

    GestureRecognizer recognizer;

    // Use this for initialization
    void Awake()
    {
        Instance = this;

        // Set up a GestureRecognizer to detect Select gestures.
        recognizer = new GestureRecognizer();
        recognizer.Tapped += (args) =>
        {
            if (FocusedObject.name == "Sphere")
            {
                Debug.Log("blokje tabed");
            }
        };
        recognizer.StartCapturingGestures();
    }

    // Update is called once per frame
    void Update()
    {
        // Figure out which hologram is focused this frame.
        GameObject oldFocusObject = FocusedObject;

        // Do a raycast into the world based on the user's
        // head position and orientation.
        var headPosition = Camera.main.transform.position;
        var gazeDirection = Camera.main.transform.forward;

        RaycastHit hitInfo;
        if (Physics.Raycast(headPosition, gazeDirection, out hitInfo))
        {
            // If the raycast hit a hologram, use that as the focused object.
            FocusedObject = hitInfo.collider.gameObject;
        }
        else
        {
            // If the raycast did not hit a hologram, clear the focused object.
            FocusedObject = null;
        }

        // If the focused object changed this frame,
        // start detecting fresh gestures again.
        if (FocusedObject != oldFocusObject)
        {
            recognizer.CancelGestures();
            recognizer.StartCapturingGestures();
        }
    }
    void OnEnable()
    {
        WorldCursor.OnClicked += Teleport;
        WorldCursor.ResetWorld += Reset;
        foreach (var Comp in this.GetComponentsInChildren<Renderer>() )
        {
            Comp.enabled = false;
        }
        
            
            //subscribe op het event
    }


    void OnDisable()
    {
        WorldCursor.OnClicked -= Teleport; //unsubscribe op het event
        WorldCursor.ResetWorld -= Reset;
    }


    void Teleport(Vector3 pos)
    {
        
        

        this.transform.position = pos;
        foreach (var Comp in this.GetComponentsInChildren<Renderer>())
        {
            Comp.enabled = true;
        }

    }
    void Reset()
    {
        foreach (var Comp in this.GetComponentsInChildren<Renderer>())
        {
            Comp.enabled = false;
        }
    }
}
