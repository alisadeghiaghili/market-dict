package com.marketdict.app;

import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.util.Locale;

@CapacitorPlugin(name = "NativeTTS")
public class NativeTTSPlugin extends Plugin {
    private TextToSpeech tts;
    private boolean isInitialized = false;
    private PluginCall activeCall = null;

    @Override
    public void load() {
        initTTS(null);
    }

    private synchronized void initTTS(Runnable onReady) {
        if (tts != null && isInitialized) {
            if (onReady != null) onReady.run();
            return;
        }

        try {
            tts = new TextToSpeech(getContext(), status -> {
                if (status == TextToSpeech.SUCCESS) {
                    isInitialized = true;
                    setupUtteranceListener();
                    if (onReady != null) onReady.run();
                } else {
                    isInitialized = false;
                    if (onReady != null) onReady.run();
                }
            });
        } catch (Exception e) {
            isInitialized = false;
            if (onReady != null) onReady.run();
        }
    }

    private void setupUtteranceListener() {
        if (tts == null) return;
        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override
            public void onStart(String utteranceId) {}

            @Override
            public void onDone(String utteranceId) {
                resolveActiveCall(true);
            }

            @Override
            public void onError(String utteranceId) {
                resolveActiveCall(false);
            }

            @Override
            public void onStop(String utteranceId, boolean interrupted) {
                resolveActiveCall(false);
            }
        });
    }

    private synchronized void resolveActiveCall(boolean completed) {
        if (activeCall != null) {
            PluginCall call = activeCall;
            activeCall = null;
            try {
                JSObject ret = new JSObject();
                ret.put("completed", completed);
                call.resolve(ret);
            } catch (Exception ignored) {}
        }
    }

    @PluginMethod
    public void speak(PluginCall call) {
        String text = call.getString("text", "");
        String lang = call.getString("lang", "fa");
        Double rateVal = call.getDouble("rate", 1.0);
        float rate = rateVal != null ? rateVal.floatValue() : 1.0f;

        if (text == null || text.trim().isEmpty()) {
            JSObject ret = new JSObject();
            ret.put("completed", true);
            call.resolve(ret);
            return;
        }

        resolveActiveCall(false);

        if (tts == null || !isInitialized) {
            initTTS(() -> performSpeak(text, lang, rate, call));
        } else {
            performSpeak(text, lang, rate, call);
        }
    }

    private void performSpeak(String text, String lang, float rate, PluginCall call) {
        if (tts == null || !isInitialized) {
            JSObject ret = new JSObject();
            ret.put("completed", false);
            ret.put("error", "TTS not initialized");
            call.resolve(ret);
            return;
        }

        try {
            Locale targetLocale;
            if ("en".equalsIgnoreCase(lang) || "en-US".equalsIgnoreCase(lang) || "en_US".equalsIgnoreCase(lang)) {
                targetLocale = Locale.US;
                tts.setLanguage(targetLocale);
            } else {
                targetLocale = new Locale("fa", "IR");
                int res = tts.setLanguage(targetLocale);
                if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {
                    tts.setLanguage(new Locale("fa"));
                }
            }

            tts.setSpeechRate(Math.max(0.6f, Math.min(2.0f, rate)));
            activeCall = call;
            String utteranceId = "utterance_" + System.currentTimeMillis();
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, utteranceId);
        } catch (Exception e) {
            resolveActiveCall(false);
            call.reject("Native TTS error: " + e.getMessage());
        }
    }

    @PluginMethod
    public void stop(PluginCall call) {
        resolveActiveCall(false);
        if (tts != null) {
            try {
                tts.stop();
            } catch (Exception ignored) {}
        }
        JSObject ret = new JSObject();
        ret.put("stopped", true);
        call.resolve(ret);
    }

    @Override
    protected void handleOnDestroy() {
        if (tts != null) {
            try {
                tts.stop();
                tts.shutdown();
            } catch (Exception ignored) {}
            tts = null;
        }
        super.handleOnDestroy();
    }
}
